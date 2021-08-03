


# AnalyzingContext Vue + restAPI version



## Main Feature

* Make Given When Then Cases using Mindmap!!!
* Make MC/DC cases from pseudo code...





## How to install your server



* pull this code to your server which is installed web server 
* frontend setting 
  * go to `/frontend` directory
  * `npm install` 
  * `npm run build`
  * set web server root directory to `/frontend/dist`
  * start web server



* backend setting 

  * check 5000 port is opened (it should be opened)
  * go to `/backend` directory
  * modify `config.py` 
    * change base_url 

  ```
  class Settings(BaseSettings):
      app_name: str = "AnalyzingContext"
      base_url: str = '[your url]'
  ```

  

  * `docker build -t [your server name] .`
  * `docker run -p 5000:5000 [your server name]` 

  



## History





### 2021/08/03

* change pairing engine "pypair.py" 
  * it is pure python pairing engine, not depend on version or outer API
* change backend framework
  * flask --> FASTAPI
  * use Nginx Unit for MSI





### 2020/09/13

* Divide whole program with frontend and backend part. 
* change backend
    * request.form ⇨ request.json
    * add flask_cors
