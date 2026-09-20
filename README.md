# HTTP Polling vs WebSocket 멀티플레이어 게임 데모

GDGoC 백엔드 발표와 실습을 위해 만든 작은 멀티플레이어 게임 예제입니다. 같은 게임 규칙과 화면을 두 가지 통신 방식으로 구현해, **HTTP Polling**과 **WebSocket**의 차이를 코드와 실행 중인 화면에서 직접 비교할 수 있습니다.

플레이어는 이름을 입력해 게임에 참가하고, `WASD` 또는 방향키로 움직입니다. 한 브라우저에서 움직인 위치는 다른 브라우저에서도 확인할 수 있으며, 브라우저를 닫으면 해당 플레이어가 게임 화면에서 사라집니다.

이 프로젝트의 목표는 완성도 높은 게임 서버를 만드는 것이 아니라, 다음 질문에 답하는 것입니다.

- HTTP 요청/응답만으로 실시간에 가까운 상태 동기화를 만들면 어떤 요청 흐름이 생길까?
- WebSocket의 지속 연결과 서버 브로드캐스트는 코드에서 어떻게 보일까?
- 폴링 간격이 갱신 지연과 서버 요청 수에 어떤 영향을 줄까?

## 구성

```text
.
├── websocket-server/       # 발표용 WebSocket 멀티플레이어 게임
├── polling-server/         # 같은 게임을 HTTP Polling으로 구현한 버전
├── websocket-complete/     # WebSocket 실습의 완성 참고 구현
└── presentation/           # 발표 스크립트와 PDF 자료
```

각 게임 디렉터리는 서로 독립적으로 실행됩니다. 디렉터리 간 코드 공유, 별도 프런트엔드 개발 서버, 데이터베이스는 사용하지 않습니다.

## 핵심 비교

| 항목 | HTTP Polling | WebSocket |
| --- | --- | --- |
| 연결 방식 | 상태가 필요할 때마다 HTTP 요청 | 한 번 연결한 뒤 지속 연결 유지 |
| 상태 수신 | 클라이언트가 `GET /api/state`를 반복 호출 | 서버가 상태 변경 시 연결된 클라이언트에 전송 |
| 이동 전송 | `POST /api/move` | `move` JSON 메시지 |
| 다른 플레이어의 이동 확인 | 다음 폴링 응답을 받을 때 | 서버의 브로드캐스트 메시지를 받을 때 |
| 관찰 포인트 | 폴링 주기와 `stateRequests` 증가량 | 연결 수, 수신/송신 메시지 수 |

두 구현 모두 서버가 플레이어 ID와 공유 상태를 관리합니다. 클라이언트는 표시 이름만 보내거나, 서버에서 발급받은 ID를 후속 HTTP 요청에 사용합니다. 게임 영역은 `640 × 360`이고 플레이어 위치는 서버에서 게임 영역 안으로 제한합니다.

## 기술 스택

- Python 3.11+
- FastAPI
- Uvicorn
- FastAPI 기본 WebSocket 지원
- Vanilla HTML / CSS / JavaScript
- 서버 프로세스 메모리 기반 상태

React, Socket.IO, Redis, 데이터베이스, SSE 등은 사용하지 않습니다. 발표 중 통신 흐름이 소스 코드에서 바로 보이도록 단순하게 구성했습니다.

## 빠른 실행

demo 배포 URL:
- websocket: http://gdg-kes-websocket.duckdns.org/websocket/
- polling: http://gdg-kes-websocket.duckdns.org/polling/

### 1. WebSocket 발표용 서버

```powershell
cd websocket-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

브라우저에서 <http://localhost:8000>을 열고, 다른 탭 또는 창에서도 같은 주소를 열어 서로 다른 이름으로 참가합니다.

### 2. HTTP Polling 서버

```powershell
cd polling-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 3. WebSocket 완성 참고 구현

```powershell
cd websocket-complete
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

macOS/Linux에서는 가상환경 활성화 명령을 `source .venv/bin/activate`로 바꾸면 됩니다.

## WebSocket 흐름

`websocket-server`와 `websocket-complete`는 모두 `/ws` 엔드포인트를 사용합니다. 로컬 개발 시 클라이언트는 `/websocket/ws` 경로로 연결하며, 서버는 두 경로를 모두 제공해 배포 경로도 지원합니다.

1. 브라우저가 WebSocket 연결을 열고 참가 메시지를 보냅니다.
2. 서버가 연결을 수락하고, 서버 생성 ID·이름·초기 좌표를 메모리에 저장합니다.
3. 키 입력마다 브라우저가 새 좌표를 `move` 메시지로 전송합니다.
4. 서버가 좌표를 검증·제한한 뒤, 모든 활성 WebSocket 연결에 전체 플레이어 상태를 브로드캐스트합니다.
5. 연결이 끊기면 서버가 해당 플레이어를 제거하고 변경된 상태를 다시 브로드캐스트합니다.

클라이언트에서 서버로 보내는 메시지:

```json
{ "type": "join", "name": "Alice" }
```

```json
{ "type": "move", "x": 120, "y": 200 }
```

서버에서 모든 연결에 보내는 상태 메시지:

```json
{
  "type": "state",
  "players": [
    { "id": "abc123", "name": "Alice", "x": 120, "y": 200 }
  ]
}
```

핵심 수업 코드는 각 WebSocket 프로젝트의 `app.py`에 있습니다. `websocket_endpoint`에서 `accept`, `receive_json`, 연결 해제 처리를 확인하고, `broadcast_state`의 `for connection in active_connections` 반복문에서 브로드캐스트가 실제로 어떻게 이루어지는지 볼 수 있습니다.

## HTTP Polling 흐름

`polling-server`에는 WebSocket 또는 서버 푸시 기능이 없습니다. 참가 후 브라우저는 일정 주기로 상태를 요청하고, 다른 플레이어의 변경 사항은 다음 상태 응답에서 확인합니다.

| API | 설명 |
| --- | --- |
| `POST /api/join` | `{ "name": "Alice" }`로 참가하고 서버 생성 `playerId`를 받습니다. |
| `POST /api/move` | `playerId`, `x`, `y`를 보내 자신의 위치를 갱신합니다. |
| `GET /api/state` | 현재 모든 플레이어 목록을 반환합니다. |
| `POST /api/leave` | 브라우저를 떠나는 플레이어를 제거합니다. |

폴링 주기는 [polling-server/static/game.js](polling-server/static/game.js)의 맨 위에 있는 다음 상수로 조절합니다.

```javascript
const POLL_INTERVAL_MS = 100;
```

발표 중 값을 `1000`, `500`, `100`으로 바꾼 뒤 페이지를 새로고침하면, 화면 갱신 반응성과 `/api/state` 요청 빈도의 차이를 확인할 수 있습니다.

## 메트릭 대시보드

두 서버 모두 가벼운 인메모리 메트릭을 제공합니다. 메트릭을 초기화해도 플레이어와 게임 상태는 지워지지 않습니다.

| 주소 | 기능 |
| --- | --- |
| `GET /api/metrics` | JSON 형식의 현재 메트릭 조회 |
| `POST /api/metrics/reset` | 카운터와 업타임 기준 시점 초기화 |
| `/websocket/metrics` | WebSocket 버전의 간단한 메트릭 화면 |
| `/polling/metrics` | Polling 버전의 간단한 메트릭 화면 |

WebSocket 버전은 현재 연결 수, 총 연결 수, 수신 메시지, 참가/이동 메시지, 연결별 송신 메시지 수를 기록합니다. 한 번의 상태 갱신이 10개 연결에 전송되면 송신 메시지는 10건으로 계산됩니다.

Polling 버전은 전체 API 요청 수와 참가·이동·상태 폴링·퇴장 요청 수를 기록합니다. 특히 여러 클라이언트를 열고 폴링 주기를 줄이면 `stateRequests`가 빠르게 증가하는 모습을 확인할 수 있습니다. 폴링 요청이 많아도 터미널이 과도하게 출력되지 않도록 이 버전에서는 Uvicorn 접근 로그를 끕니다.

## 발표·실습 활용 순서

1. `websocket-server`를 실행해 두 개 이상의 브라우저 창으로 실시간 이동 동기화를 보여줍니다.
2. `app.py`의 WebSocket 연결 수락, 메시지 수신, 상태 브로드캐스트 부분을 코드와 함께 설명합니다.
3. `polling-server`를 실행해 같은 조작을 보여주고, `POLL_INTERVAL_MS`를 바꿔 요청 빈도와 갱신 지연을 비교합니다.
4. 각 메트릭 화면 또는 `/api/metrics` 응답을 보며 실제 요청·메시지 수를 비교합니다.
5. 실습에서는 `websocket-complete`를 WebSocket 브로드캐스트 완성본의 참고 코드로 사용합니다.

`await websocket.receive_json()`은 HTTP 폴링이 아닙니다. 이미 맺어진 WebSocket 연결에서 다음 메시지가 도착할 때까지 비동기로 기다리는 동작이며, 매번 새 HTTP 요청을 생성하는 폴링과 구별됩니다.

## 제약과 의도된 단순화

이 코드는 교육·데모 용도입니다. 게임 상태는 메모리에만 있으므로 서버를 재시작하면 사라지고, 다중 서버 인스턴스 간 상태 공유도 지원하지 않습니다. 인증, 방, 충돌 판정, 점수, 채팅, 영속 저장소 같은 기능은 의도적으로 포함하지 않았습니다.

Google Cloud VM 등에 배포하기 전에 HTTPS/WSS 구성, 외부 접근 정책, 프로세스 관리, 오류 처리와 운영 모니터링을 별도로 검토해야 합니다.

## 발표 자료

90분 세션의 슬라이드별 진행 내용은 [presentation/script.txt](presentation/script.txt)에, 발표용 PDF는 [presentation/presentation.pdf](presentation/presentation.pdf)에 있습니다.
