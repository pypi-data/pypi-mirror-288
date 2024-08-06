# API_CANVAS_LMS

Una biblioteca para ADDA Canvas LMS

# Estructura del Proyecto

```
|--api_canvas_lms/        <-- Archivos de python
|     |--account.py         
|     |--adda.py         
|     |--discussion_topic.py         
|     |--module.py          
|     |--user.py          
|--setup.py               <-- Define el Python build
```

# Uso

Un ejemplo de como usar la biblioteca

```
import settings
import logging
import logging_config

# Ensure the logging configuration is set up
logging_config.setup_logging()

import api_canvas_lms.adda as adda 
```

```
# Create a logger for this module
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    course_id = "66666"  # ID Course

    #''' 
    logger.info("Start process ... !")
    mccsa = adda.BasicModuleCourseCanvasADDA(course_id, settings.TOKEN)
    status, data = mccsa.is_valid_structure()    
    logger.info(status)
    logger.info(data)
    #'''
```

