# Infinity Translator

<div align="center">🌐 <a href="/docs/README_zh-Hans.md">简体中文</a> | <a href="/docs/README_zh-Hant.md">繁體中文</a> | <a href="/docs/README_ja.md">日本語</a> | <a href="/docs/README_fr.md">Français</a> | <a href="/docs/README_kr.md">한국어</a> | <a href="/docs/README_ru.md">Русский</a></div>

---
Infinity Translator는 대형 언어 모델을 활용하여 긴 텍스트를 번역하는 소프트웨어이며, 현대적이고 아름다운 UI 인터페이스를 제공합니다. 큰 문서를 적절히 분할하고 전처리하여 여러 언어로 번역할 수 있습니다.

![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot2.png)
![image](https://github.com/Arlecchino745/infinity_translator/blob/main/docs/img/screenshot.png)

## 기능 ✨

- 문서 길이 제한 없이 대용량 문서 번역 지원 📄
- 번역의 시각적 표현을 최적화하기 위해 Markdown 문서 전처리 🎨
- 번역 진행 상황을 실시간으로 표시하고 번역 결과를 자동으로 저장 ⏱️

## 빠른 시작!

**알림: 불행히도 일부 기술적 문제로 인해 이 릴리스는 OpenRouter를 통한 Google Gemini 2.0 Flash를 사용한 번역 작업만 지원합니다. 이 문제는 후속 릴리스에서 우선적으로 해결될 것입니다.**

1. [Releases](https://github.com/Arlecchino745/infinity_translator/releases) 페이지에서 최신 릴리스를 다운로드합니다.
2. 다운로드한 zip 파일을 압축 해제합니다.
3. _internal 폴더를 열고, .env.example을 복사하여 .env로 이름을 변경한 다음 API 키를 입력합니다.
4. `infinity_translator.exe`를 실행하여 애플리케이션을 시작합니다.

## 소스 코드에서 시작 (개발)

1. 프로젝트를 복제하고 프로젝트 폴더로 전환합니다:
```bash
# GitHub에서 로컬 머신으로 프로젝트 코드 복제
git clone https://github.com/Arlecchino745/infinity_translator.git
# 프로젝트 디렉토리로 전환
cd infinity_translator
```

2. 종속성 설치: 적절한 Python 버전을 선택하는 데 주의하십시오. 이 프로젝트는 Python 3.12에서 정상적으로 실행되는 것으로 알려져 있습니다.
```bash
# .venv라는 가상 환경 생성
python -m venv .venv
# 가상 환경 활성화 (Windows 시스템용)
.\.venv\Scripts\Activate
# 가상 환경 활성화 (Linux&Mac용)
source ./.venv/bin/activate
# 프로젝트에 필요한 종속성 라이브러리 설치
pip install -r requirements.txt
```

3. API 키 구성: 프로젝트 폴더의 `.env.example` 파일을 참조하십시오. ⚙️
   - `.env.example` 파일을 `.env`로 복사하고 API 키를 입력하십시오.

4. (선택 사항) config 폴더의 settings.json에 있는 주석에 따라 개인화된 구성을 만드십시오. 🛠️
   - 사용자 정의 구성이 필요한 경우 `config/settings.json.example` 파일을 참조하십시오.

5. 위의 단계를 완료한 후 실행합니다:
```bash
# 웹 애플리케이션 시작
python web_app.py
```
그런 다음 브라우저의 주소 표시줄에 `localhost:8000` 또는 `127.0.0.1:8000`을 입력하고 확인합니다. 🎉

### 애플리케이션 설정 구성 (소스 코드에서 시작하는 경우만 해당)⚙️

프로젝트에는 두 개의 구성 파일이 있습니다:
- `config/settings.json` - 기본 구성 파일, 수정하지 않아야 함
- `config/settings.json.example` - 구성 템플릿 파일 참조용

고급 사용자 정의 구성(예: 새 모델 또는 서비스 제공업체 추가)이 필요한 경우 다음 단계를 따르십시오:

1. `config/settings.json` 파일을 복사하고 `config/settings.user.json`으로 이름을 바꿉니다:
   ```bash
   # 기본 구성 파일을 사용자 정의 구성 파일로 복사
   cp config/settings.json config/settings.user.json
   ```

2. `config/settings.user.json` 파일의 구성을 수정합니다
   - 필요에 따라 `settings.user.json` 파일을 편집합니다(예: 새 모델 추가 또는 매개변수 조정).

3. 애플리케이션은 settings.user.json을 우선적으로 로드하므로 사용자 정의 구성은 Git에 의해 추적되지 않습니다
   - 이렇게 하면 사용자 정의 구성이 Git에 의해 원격 저장소에 커밋되는 것을 방지할 수 있습니다.

## 기술 스택 💻

- 백엔드: FastAPI + Uvicorn
- 프론트엔드: Vue.js + Axios
- 번역: LangChain + OpenAI API
- 빌드: PyInstaller

## 라이선스 📄

프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다.

## AIGC 선언

이 프로젝트는 AI가 지원됩니다. 의도하지 않은 침해가 있는 경우 저자에게 연락하십시오.