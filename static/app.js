const { createApp } = Vue

const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            providers: {},
            selectedProvider: '',
            selectedModel: null,
            showModelList: false,
            showProviderList: false,
            showLanguageList: false,
            selectedFile: null,
            isDragging: false,
            isTranslating: false,
            error: null,
            progress: 0,
            translatedChunks: 0,
            totalChunks: 0,
            startTime: null,
            progressStatus: 'Preparing...',
            languageList: [],
            selectedLanguage: null
        }
    },
    computed: {
        estimatedTimeRemaining() {
            if (!this.startTime || !this.translatedChunks) return 'Calculating...';
            
            const elapsed = (Date.now() - this.startTime) / 1000;
            const avgTimePerChunk = elapsed / this.translatedChunks;
            const remaining = this.totalChunks - this.translatedChunks;
            const estimatedSeconds = avgTimePerChunk * remaining;
            
            if (estimatedSeconds < 60) {
                return `About ${Math.ceil(estimatedSeconds)} seconds`;
            } else {
                return `About ${Math.ceil(estimatedSeconds / 60)} minutes`;
            }
        },
        currentProvider() {
            return this.providers[this.selectedProvider] || null;
        }
    },
    methods: {
        async loadProviders() {
            try {
                const response = await axios.get('/api/providers');
                this.providers = response.data.providers;
                this.selectedProvider = response.data.active_provider;
                
                // 设置默认的Model为当前Provider的第一个Model
                if (this.selectedProvider && this.providers[this.selectedProvider]) {
                    const provider = this.providers[this.selectedProvider];
                    if (provider.models && provider.models.length > 0) {
                        this.selectedModel = provider.models[0];
                    }
                }
            } catch (error) {
                this.error = 'Failed to load provider information';
                console.error('Provider loading error:', error);
            }
        },
        async loadLanguages() {
            try {
                const response = await axios.get('/api/languages');
                this.languageList = response.data.language_list;
                this.selectedLanguage = this.languageList.find(lang => lang.code === response.data.target_language) || this.languageList[0];
            } catch (error) {
                this.error = 'Failed to load language information';
                console.error('Language loading error:', error);
            }
        },
        async changeProvider(event) {
            const providerId = event.target.value;
            this.selectProvider(providerId);
        },
        toggleModelList() {
            this.showModelList = !this.showModelList;
        },
        toggleProviderList() {
            this.showProviderList = !this.showProviderList;
        },
        toggleLanguageList() {
            this.showLanguageList = !this.showLanguageList;
        },
        selectModel(model) {
            this.selectedModel = model;
            this.showModelList = false;
        },
        selectProvider(providerId) {
            this.selectedProvider = providerId;
            this.showProviderList = false;
            // Reset model selection when provider changes
            this.selectedModel = null;
            
            // Call API to change provider
            axios.post('/api/set-provider', {
                provider: providerId
            }).catch(error => {
                this.error = 'Failed to change provider';
                console.error('Provider change error:', error);
            });
        },
        selectLanguage(language) {
            this.selectedLanguage = language;
            this.showLanguageList = false;
            
            // Call API to change target language
            axios.post('/api/set-language', {
                language: language.code
            }).catch(error => {
                this.error = 'Failed to change target language';
                console.error('Language change error:', error);
            });
        },
        handleFileDrop(event) {
            event.preventDefault();
            this.isDragging = false;
            const file = event.dataTransfer.files[0];
            if (file) {
                this.handleFile(file);
            }
        },
        handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                this.handleFile(file);
            }
        },
        handleFile(file) {
            // Validate file type
            const allowedTypes = ['.txt', '.md', '.json', '.csv'];
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            
            if (!allowedTypes.includes(fileExtension)) {
                this.error = `Unsupported file type. Please select a file with one of these extensions: ${allowedTypes.join(', ')}`;
                return;
            }
            
            // Validate file size (e.g., max 50MB)
            const maxSize = 50 * 1024 * 1024; // 50MB in bytes
            if (file.size > maxSize) {
                this.error = 'File size too large. Please select a file smaller than 50MB.';
                return;
            }
            
            this.selectedFile = file;
            this.error = null;
        },
        formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },
        async translate() {
            if (!this.selectedFile || !this.selectedModel) return;
            
            this.isTranslating = true;
            this.error = null;
            this.progress = 0;
            this.translatedChunks = 0;
            this.totalChunks = 0;
            this.startTime = Date.now();
            this.progressStatus = 'Preparing translation...';

            const formData = new FormData();
            formData.append('file', this.selectedFile);
            formData.append('model_name', this.selectedModel.id);

            // Setup progress tracking
            let eventSource = null;
            
            try {
                // Start progress monitoring
                eventSource = new EventSource('/translate-progress');
                eventSource.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        this.progress = data.progress || 0;
                        this.translatedChunks = data.translated_chunks || 0;
                        this.totalChunks = data.total_chunks || 0;
                        this.progressStatus = data.status || 'Processing...';
                    } catch (parseError) {
                        console.error('Progress parsing error:', parseError);
                    }
                };
                
                eventSource.onerror = (error) => {
                    console.error('EventSource error:', error);
                };

                // Start translation
                const response = await axios.post('/translate', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    responseType: 'blob',
                    onUploadProgress: (progressEvent) => {
                        if (progressEvent.total) {
                            const uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                            this.progressStatus = `Uploading file... ${uploadProgress}%`;
                            this.progress = Math.min(uploadProgress * 0.1, 10); // Upload is 10% of total progress
                        }
                    },
                    timeout: 300000 // 5 minutes timeout
                });

                // Close progress monitoring
                if (eventSource) {
                    eventSource.close();
                }

                // Handle successful response
                const contentDisposition = response.headers['content-disposition'];
                let filename = 'translated.md';
                if (contentDisposition) {
                    const matches = /filename="([^"]*)"/.exec(contentDisposition);
                    if (matches && matches[1]) {
                        filename = matches[1];
                    }
                }

                // Create download link
                const blob = new Blob([response.data], { type: 'text/markdown' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = filename;
                link.style.display = 'none';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);

                // Show success message
                this.progressStatus = 'Translation completed successfully!';
                this.progress = 100;
                
                // Reset after a delay
                setTimeout(() => {
                    this.resetTranslationState();
                }, 3000);

            } catch (error) {
                console.error('Translation error:', error);
                
                // Close progress monitoring
                if (eventSource) {
                    eventSource.close();
                }
                
                let errorMessage = 'An unexpected error occurred during translation';
                
                if (error.response) {
                    // Server responded with error status
                    if (error.response.data instanceof Blob) {
                        try {
                            const text = await error.response.data.text();
                            const errorData = JSON.parse(text);
                            errorMessage = errorData.message || errorMessage;
                        } catch (parseError) {
                            errorMessage = `Server error: ${error.response.status}`;
                        }
                    } else if (error.response.data && error.response.data.message) {
                        errorMessage = error.response.data.message;
                    } else {
                        errorMessage = `Server error: ${error.response.status}`;
                    }
                } else if (error.request) {
                    // Network error
                    errorMessage = 'Network error. Please check your connection and try again.';
                } else if (error.code === 'ECONNABORTED') {
                    // Timeout error
                    errorMessage = 'Translation timeout. The file might be too large or the server is busy.';
                }
                
                this.error = errorMessage;
                this.resetTranslationState();
            }
        },
        resetTranslationState() {
            this.isTranslating = false;
            this.progress = 0;
            this.translatedChunks = 0;
            this.totalChunks = 0;
            this.startTime = null;
            this.progressStatus = 'Ready to start translation';
        },
        // Handle drag events
        handleDragOver(event) {
            event.preventDefault();
            this.isDragging = true;
        },
        handleDragLeave(event) {
            event.preventDefault();
            // Only set isDragging to false if we're leaving the drop zone entirely
            if (!event.currentTarget.contains(event.relatedTarget)) {
                this.isDragging = false;
            }
        },
        // Close dropdown when clicking outside
        handleClickOutside(event) {
            const isClickingOutsideProvider = this.showProviderList && 
                !this.$refs.providerDropdown?.contains(event.target);
            const isClickingOutsideModel = this.showModelList && 
                !this.$refs.modelDropdown?.contains(event.target);
            const isClickingOutsideLanguage = this.showLanguageList &&
                !this.$refs.languageDropdown?.contains(event.target);
                
            if (isClickingOutsideProvider) {
                this.showProviderList = false;
            }
            
            if (isClickingOutsideModel) {
                this.showModelList = false;
            }

            if (isClickingOutsideLanguage) {
                this.showLanguageList = false;
            }
        },
        // Keyboard navigation for accessibility
        handleKeydown(event) {
            if (event.key === 'Escape') {
                this.showModelList = false;
                this.showProviderList = false;
                this.showLanguageList = false;
                this.error = null;
            }
        },
        // Add method for auto scrolling to 60% of the page
        autoScrollToPosition() {
            // Wait for the page to fully render
            this.$nextTick(() => {
                setTimeout(() => {
                    const scrollPosition = document.body.scrollHeight * 0.34;
                    window.scrollTo({
                        top: scrollPosition,
                        behavior: 'smooth'
                    });
                }, 500); // Small delay to ensure everything is rendered
            });
        }
    },
    mounted() {
        this.loadProviders();
        this.loadLanguages();
        
        // Add global event listeners
        document.addEventListener('click', this.handleClickOutside);
        document.addEventListener('keydown', this.handleKeydown);
        
        // Prevent default drag behaviors on the entire document
        document.addEventListener('dragover', (e) => e.preventDefault());
        document.addEventListener('drop', (e) => e.preventDefault());
        
        // Auto scroll to 60% of the page
        this.autoScrollToPosition();
    },
    beforeUnmount() {
        // Clean up event listeners
        document.removeEventListener('click', this.handleClickOutside);
        document.removeEventListener('keydown', this.handleKeydown);
        document.removeEventListener('dragover', (e) => e.preventDefault());
        document.removeEventListener('drop', (e) => e.preventDefault());
    }
})

app.mount('#app')

