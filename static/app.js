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
            translatedText: '',
            isTranslating: false,
            error: null
        }
    },
    computed: {
        formattedTranslation() {
            return this.translatedText
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/\n/g, '<br>')
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
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                this.error = '文件大小不能超过10MB';
                return;
            }
            this.selectedFile = file;
            this.error = null;
        },
        async translate() {
            if (!this.selectedFile || !this.selectedModel) return;
            
            this.isTranslating = true;
            this.error = null;

            const formData = new FormData();
            formData.append('file', this.selectedFile);

            try {
                const response = await axios.post('/translate', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                if (response.data.status === 'success') {
                    this.translatedText = response.data.translated_text;
                } else {
                    throw new Error(response.data.message || '翻译失败');
                }
            } catch (error) {
                this.error = error.response?.data?.message || error.message || '发生未知错误';
                this.translatedText = '';
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
