# Meal Provider 🍌

## 開發流程

1. 使用 vscode開 devcontainer 起來

2. database init

    ```sh
    flask db init
    ```

3. 塞一些假資料
    在 vscode 的 terminal 執行

    ```sh
    flask db add_mock
    ```

4. Run dev server

    ```sh
    flask run
    ```

5. visit
    http://localhost:5000

## Utilities

* 重置資料庫 (如果db欄位有更動的話，要重新建立)
    `flask db init`
