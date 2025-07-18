+--------------+            +---------------------+            +-------------------+
|   Frontend   |  <--->     |     FastAPI (main.py)|  <--->     |     LiveKit Server |
| (in browser) |  token     |   /create-room       |  token     | (Cloud or Local)   |
+--------------+            +---------------------+            +-------------------+
       |                                                               ^
       | wss:// connect                                                |
       v                                                               |
+-------------------+           +--------------------------+          |
|   agent.py (bot)  | <-------- |  Token from FastAPI      | ---------+
| (Python client)   |           +--------------------------+
+-------------------+

