let cursorX = 0; // カーソルのX位置
let cursorY = 0; // カーソルのY位置
let cursorSpeed = 10; // カーソル移動速度
let scrollSpeed = 10; // スクロール速度
let previousButtonStates = []; // ボタンの前回の状態を記録

// ゲームパッド接続時の処理
window.addEventListener("gamepadconnected", (event) => {
    console.log("Gamepad connected:", event.gamepad);
    previousButtonStates = new Array(18).fill(false); // ボタンの状態を初期化
    gameLoop(); // ゲームループ開始
});

// ゲームパッドが切断された場合の処理
window.addEventListener("gamepaddisconnected", (event) => {
    console.log("Gamepad disconnected:", event.gamepad);
});

// ゲームパッドの入力チェック
function gameLoop() {
    const gamepad = navigator.getGamepads()[0]; // 1台目のゲームパッドを取得
    if (gamepad) {
        // 左スティックでカーソル移動
        const xAxis = gamepad.axes[0]; // 左スティックの左右
        const yAxis = gamepad.axes[1]; // 左スティックの上下

        // スティック入力に基づいてカーソル位置を更新
        cursorX += xAxis * cursorSpeed;
        cursorY += yAxis * cursorSpeed;

        // 画面内にカーソルが収まるように制限
        cursorX = Math.max(0, Math.min(window.innerWidth, cursorX));
        cursorY = Math.max(0, Math.min(window.innerHeight, cursorY));

        // ログ：カーソル位置
        console.log(`カーソル位置 - X: ${cursorX}, Y: ${cursorY}`);

        // カーソルの描画と形状変更
        updateCursor();

        // 右スティックでスクロール操作
        const scrollXAxis = gamepad.axes[2]; // 右スティックの左右
        const scrollYAxis = gamepad.axes[3]; // 右スティックの上下

        if (Math.abs(scrollXAxis) > 0.1 || Math.abs(scrollYAxis) > 0.1) {
            // スティックの入力値がしきい値を超えている場合にスクロール
            window.scrollBy(scrollXAxis * scrollSpeed, scrollYAxis * scrollSpeed);
            console.log(`スクロール - X: ${scrollXAxis * scrollSpeed}, Y: ${scrollYAxis * scrollSpeed}`);
        }

        // ボタンの状態をチェック
        gamepad.buttons.forEach((button, index) => {
            const wasPressed = previousButtonStates[index]; // 前回の状態
            const isPressed = button.pressed; // 今回の状態

            console.log(`ボタン ${index} - 前回: ${wasPressed}, 今回: ${isPressed}`);

            if (isPressed && !wasPressed) {
                if (index === 0) { // 0は「○」ボタン
                    console.log("○ボタンが押されました！（決定）");
                }

                if (index === 1) { // 1は「×」ボタン（左クリックに対応）
                    console.log("×ボタンが押されました！（左クリック）");
                    simulateMouseClick(cursorX, cursorY); // マウス左クリックをシミュレート
                }
            }

            // 状態を更新
            previousButtonStates[index] = isPressed;
        });

        // 毎フレーム処理を繰り返す
        requestAnimationFrame(gameLoop);
    }
}

// カーソルを画面に描画する関数
function updateCursor() {
    let cursor = document.getElementById('cursor');
    if (!cursor) {
        cursor = document.createElement('div');
        cursor.id = 'cursor';
        cursor.style.position = 'absolute';
        cursor.style.width = '20px';
        cursor.style.height = '20px';
        cursor.style.border = '2px solid black';
        cursor.style.borderRadius = '50%';
        cursor.style.backgroundColor = 'transparent';
        cursor.style.pointerEvents = 'none'; // カーソル自体はクリックを防止
        document.body.appendChild(cursor);

        // マウスカーソルを非表示にする
        document.body.style.cursor = 'none';
    }

    // カーソルの位置を更新
    cursor.style.left = `${cursorX}px`;
    cursor.style.top = `${cursorY}px`;

    // カーソル形状を変更
    changeCursorShape(cursorX, cursorY);
}

// カーソルの形状を変更する関数
function changeCursorShape(x, y) {
    const element = document.elementFromPoint(x, y); // カーソル位置にある要素を取得
    if (element) {
        console.log(`カーソル下の要素: ${element.tagName}, id: ${element.id || 'なし'}, class: ${element.className || 'なし'}`);
    } else {
        console.log("カーソル下の要素が見つかりません");
    }

    // リンクやボタン、ポインターを持つ要素上でカーソルを変える
    if (element && (element.tagName === 'A' || element.tagName === 'BUTTON' || element.style.cursor === 'pointer')) {
        document.getElementById('cursor').style.borderColor = 'blue'; // リンクやボタン上でカーソル色変更
    } else {
        document.getElementById('cursor').style.borderColor = 'black'; // デフォルトの色に戻す
    }
}

// マウスのクリックをシミュレートする関数
function simulateMouseClick(x, y) {
    const target = document.elementFromPoint(x, y); // カーソル位置にある要素を取得
    if (target) {
        console.log(`クリック対象の要素: ${target.tagName}`);

        // クリックイベントの発火
        const mouseEvent = new MouseEvent("click", {
            bubbles: true,
            cancelable: true,
            clientX: x,
            clientY: y
        });

        target.dispatchEvent(mouseEvent); // clickイベントを発火

        // リンクの場合は、`<a>`タグのクリックイベントが発火するのを確認
        if (target.tagName === 'A' && target.href) {
            // ここでは遷移を発生させない
            console.log(`リンク先: ${target.href}`);
        }
    } else {
        console.log("クリック対象の要素がありません");
    }
}
