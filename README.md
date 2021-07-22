### 1. to run in prod server

```shell
pm2 start app.py --watch --name 12-animal-classification --interpreter python3 -- -s prod -p 30001
```

### 2. to run in service server

```shell
pm2 start app.py --watch --name 12-animal-classification --interpreter python3 -- -s service -p 30001
```

### 3. to run in test server

```shell
pm2 start app.py --watch --name 12-animal-classification --interpreter python3 -- -p 30001
```

### Output example
```shell
{
  "chicken": 10.4,
  "cow": 9.42,
  "dog": 3.73,
  "dragon": 1.48,
  "horse": 45.94,
  "monkey": 1.42,
  "mouse": 0.42,
  "pig": 2.21,
  "rabbit": 0.02,
  "sheep": 0.45,
  "snake": 24.41,
  "tiger": 0.09
}
```
