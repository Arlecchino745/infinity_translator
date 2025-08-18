const { createApp } = Vue

const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            providers: {},
            selectedProvider: '',
            selectedModel: null,
            showModelList: false,
            selectedFile: null,
            isDragging: false,
            isTranslating: false,
            error: null,
            progress: 0,
            translatedChunks: 0,
            totalChunks: 0,
            startTime: null,
            progressStatus: '准备中...'
        }
    },
    computed: {
        estimatedTimeRemaining() {
            if (!this.startTime || !this.translatedChunks) return '计算中...';
            
            const elapsed = (Date.now() - this.startTime) / 1000;
            const avgTimePerChunk = elapsed / this.translatedChunks;
            const remaining = this.totalChunks - this.translatedChunks;
            const estimatedSeconds = avgTimePerChunk * remaining;
            
            if (estimatedSeconds < 60) {
                return `约 ${Math.ceil(estimatedSeconds)} 秒`;
            } else {
                return `约 ${Math.ceil(estimatedSeconds / 60)} 分钟`;
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
            } catch (error) {
                this.error = '加载服务商信息失败';
            }
        },
        async changeProvider(event) {
            try {
                await axios.post('/api/set-provider', {
                    provider: event.target.value
                });
                this.selectedModel = null;
            } catch (error) {
                this.error = '更改服务商失败';
            }
        },
        toggleModelList() {
            this.showModelList = !this.showModelList;
        },
        selectModel(model) {
            this.selectedModel = model;
            this.showModelList = false;
        },
        handleFileDrop(event) {
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
            this.selectedFile = file;
            this.error = null;
        },
        async translate() {
            if (!this.selectedFile) return;
            
            this.isTranslating = true;
            this.error = null;

            const formData = new FormData();
            formData.append('file', this.selectedFile);
            if (this.selectedModel) {
                formData.append('model_name', this.selectedModel.id);
            }

            this.startTime = Date.now();
            this.progress = 0;
            this.translatedChunks = 0;
            
            const eventSource = new EventSource(`/translate-progress`);
            eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.progress = data.progress;
                this.translatedChunks = data.translated_chunks;
                this.totalChunks = data.total_chunks;
                this.progressStatus = data.status;
            };

            try {
                const response = await axios.post('/translate', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    responseType: 'blob',
                    onUploadProgress: (progressEvent) => {
                        this.progressStatus = '上传文件中...';
                        this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    }
                });

                eventSource.close();
                // 从响应头获取文件名
                const contentDisposition = response.headers['content-disposition'];
                let filename = 'translated.md';
                if (contentDisposition) {
                    const matches = /filename="([^"]*)"/.exec(contentDisposition);
                    if (matches && matches[1]) {
                        filename = matches[1];
                    }
                }

                // 创建下载链接
                const blob = new Blob([response.data], { type: 'text/markdown' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = filename;
                link.click();
                URL.revokeObjectURL(url);
            } catch (error) {
                let errorMessage = '发生未知错误';
                if (error.response?.data) {
                    try {
                        const blob = error.response.data;
                        const text = await blob.text();
                        const errorData = JSON.parse(text);
                        errorMessage = errorData.message || errorMessage;
                    } catch (e) {
                        errorMessage = error.message || errorMessage;
                    }
                }
                this.error = errorMessage;
            } finally {
                this.isTranslating = false;
            }
        }
    },
    mounted() {
        this.loadProviders();
    }
})

app.mount('#app')
