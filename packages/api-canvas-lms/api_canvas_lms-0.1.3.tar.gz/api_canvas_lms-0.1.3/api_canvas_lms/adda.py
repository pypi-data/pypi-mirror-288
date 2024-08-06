""" 
Programa : Module for ADDA
Fecha Creacion : 05/08/2024
Fecha Update : None
Version : 1.0.0
Actualizacion : None
Author : Jaime Gomez
"""

import logging
import pandas as pd
from .module import ModuleTemplateCourseCanvas 
from .module import  KEY_MOD_1, KEY_MOD_2
from .module import  LABEL_CLASS_MATERIALS
from .module import  TEMPLATE_SHORT_SESSION, TEMPLATE_SHORT_NRO_SESSION
from .discussion_topic import DiscussionTopic
from .user import Users , TEACHERS

# METHODOLOGY ADDA

# -*- coding: utf-8 -*-
LABEL_METHOD_ADDA_BEFORE     = "Antes de clase"  #"FASE ASÍNCRONA ( Antes )"
LABEL_METHOD_ADDA_BEFORE_POS = 1
LABEL_METHOD_ADDA_DURING     = "Durante la clase"  #"FASE SÍNCRONA ( Durante )"
LABEL_METHOD_ADDA_DURING_POS = 3
LABEL_METHOD_ADDA_AFTER      =  "Después de clase"  # "FASE ASÍNCRONA ( Después )"
LABEL_METHOD_ADDA_AFTER_POS  = 6

MODULES = "modules"

# Create a logger for this module
logger = logging.getLogger(__name__)


class ADDA :

    def __init__(self, name):
        self.name = name
        self.before = False
        self.during = False
        self.after = False

    def validate(self):
        return self.before and self.during and self.after

    def incomplete(self):
        data = list()
        if not self.before : data.append(LABEL_METHOD_ADDA_BEFORE)
        if not self.during : data.append(LABEL_METHOD_ADDA_DURING)
        if not self.after : data.append(LABEL_METHOD_ADDA_AFTER)
        return data        

class BasicModuleCourseCanvasADDA(ModuleTemplateCourseCanvas):

    def __init__(self, course_id,  access_token):
        super().__init__(course_id, access_token)

    def extract_item_adda_module_course(self, mod):

        item_adda_module = ADDA(mod["name"])

        mod_items = mod["items"] 

        if len(mod_items) > 0 :
            
            df = pd.DataFrame(mod_items)                    

            # Exist the LABEL_METHOD_ADDA_BEFORE ?
            item_adda_before = df[df["title"] == LABEL_METHOD_ADDA_BEFORE]
            item_adda_module.before = len(item_adda_before) == 1

            # Exist the LABEL_METHOD_ADDA_DURING ?
            item_adda_during = df[df["title"] == LABEL_METHOD_ADDA_DURING]        
            item_adda_module.during = len(item_adda_during) == 1

            # Exist the LABEL_METHOD_ADDA_AFTER ?
            item_adda_after = df[df["title"] == LABEL_METHOD_ADDA_AFTER]        
            item_adda_module.after = len(item_adda_after) == 1

        return item_adda_module

    
    def is_valid_structure(self, w_from = 1, w_to = 16 ):

        data = dict()

        # Validate ADDA structure
        modules = dict()
        for item in self.read_adda_module_course(w_from,w_to):
            logging.debug(f" {item.name} {item.validate()}")
            if not item.validate():
                modules[item.name] = item.incomplete()

        # Are incomplete ADDA information
        status = not bool(len(modules))

        if not status:

            # Get teacher information if ADD information is imcomplete
            users = Users(self.course_id, self.access_token)
            teachers = users.get_teachers()
            logger.debug(teachers)

            # Create response
            data[TEACHERS] = teachers
            data[MODULES] = modules

        return status, data


    def read_adda_module_course(self, w_from = 1, w_to = 16):

        module_course = list()

        # Parameters to include additional information
        params = {
#            'include[]': ['items', 'content_details']
            'include[]': ['items']
        }

        logger.debug("Begin : get module details")
        modules = self.get_modules(params)
        logger.debug("End : get module details")
        logger.debug(modules)
        
        for mod in modules:
            if (mod["name"].upper().startswith(KEY_MOD_1) or mod["name"].upper().startswith(KEY_MOD_2) ) :
                nro_week = self.get_nro_week(mod["name"])
                if  w_from <= nro_week <= w_to :
                    logger.debug(f"[{mod['position']}] : {mod['name']}")
                    module_course.append(self.extract_item_adda_module_course(mod))  

        return module_course 

class ModuleCourseCanvasADDA(BasicModuleCourseCanvasADDA):
 
    def __init__(self, course_id, template_discussion_topic, access_token):
        super().__init__(course_id, access_token)
        self.template_discussion_topic = template_discussion_topic

    def clean_module_course(self, mod, nro_week):
        flag = True
        mod_items = self.get_items(mod["id"])

        for item in mod_items:
            if (item["title"].startswith(LABEL_CLASS_MATERIALS) ) :
                flag = False
                print("DELETE ITEM ===> " , item["title"])
                self.delete_item_module(mod['id'], item["id"] )

        if flag : print("EMPTY ITEM TO DELETE")


    def config_module(self, mod): 
        """
            Configure the label of methodology ADDA
        """
        mod_items = self.get_items(mod["id"])
        df = pd.DataFrame(mod_items)
        #print("ITEMS ===> " , mod_items)

        if len(mod_items) > 0 :
  
            # Create
            if len(df[df["title"] == LABEL_METHOD_ADDA_BEFORE]) == 0:
                self.create_subheader_module(mod['id'], LABEL_METHOD_ADDA_BEFORE , LABEL_METHOD_ADDA_BEFORE_POS)
                # Refresh mod_items attributes
                mod_items = self.get_items(mod["id"])
                df = pd.DataFrame(mod_items)
            if len(df[df["title"] == LABEL_METHOD_ADDA_DURING]) == 0:
                self.create_subheader_module(mod['id'], LABEL_METHOD_ADDA_DURING , LABEL_METHOD_ADDA_DURING_POS)
                # Refresh mod_items attributes
                mod_items = self.get_items(mod["id"])
                df = pd.DataFrame(mod_items)
            if len(df[df["title"] == LABEL_METHOD_ADDA_AFTER]) == 0:
                self.create_subheader_module(mod['id'], LABEL_METHOD_ADDA_AFTER , LABEL_METHOD_ADDA_AFTER_POS)
                # Refresh mod_items attributes
                mod_items = self.get_items(mod["id"])
                df = pd.DataFrame(mod_items)
            
            # Update

        else: 
            # Module items empty
            self.create_subheader_module(mod['id'], LABEL_METHOD_ADDA_BEFORE , LABEL_METHOD_ADDA_BEFORE_POS)
            self.create_subheader_module(mod['id'], LABEL_METHOD_ADDA_DURING , LABEL_METHOD_ADDA_DURING_POS)
            self.create_subheader_module(mod['id'], LABEL_METHOD_ADDA_AFTER , LABEL_METHOD_ADDA_AFTER_POS)

    def create_discussion_topics_module(self, mod_id, content_id, pos = 1 ):
        data = {'module_item[content_id]'   : content_id ,
                'module_item[type]'         : 'Discussion',
                'module_item[position]'     : pos,
                'module_item[indent]'       : '1'}
        self.post_item(mod_id, data)

    def config_module_course(self, mod, nro_week):

        NRO_SESSION = "{:02d}".format(nro_week)
        S_NRO_SESSION = "S{:02d}".format(nro_week)

        mod_items = self.get_items(mod["id"])
        
        # print("ITEMS ===> " , pd.DataFrame(mod_items).head(10))

        if len(mod_items) > 0 :
            
            df = pd.DataFrame(mod_items)                    
            item_adda_before = df[df["title"] == LABEL_METHOD_ADDA_BEFORE]
        
            # Exist the LABEL_METHOD_ADDA_BEFORE ?
            if len(item_adda_before) == 1:
        
                pos_adda_before = item_adda_before['position'].values[0]

                # Verify if the forum before was create
                if df[df['title'].str.startswith(S_NRO_SESSION)].empty:

                    # Create discussion topic
                    dt_before = DiscussionTopic(self.course_id, self.access_token)

                    title_discussion_topic_before = \
                        self.template_discussion_topic["before"]["title"].replace(TEMPLATE_SHORT_SESSION,S_NRO_SESSION)

                    title_discussion_topic_before = \
                        title_discussion_topic_before.replace(TEMPLATE_SHORT_NRO_SESSION,NRO_SESSION)
                    
                    res_dt_before = dt_before.create_discussion_topic(title_discussion_topic_before,
                                                                    self.template_discussion_topic["before"]["message"])
                    
                    # Create link to discussion topic in module
                    self.create_discussion_topics_module(mod['id'],res_dt_before['id'], pos_adda_before+1)            

    
        # REFRESH : READ AGAIN BECAUSE POSITION CHANGE IN MODULE
        mod_items = self.get_items(mod["id"])
        #print("ITEMS ===> " , pd.DataFrame(mod_items).head())

        if len(mod_items) > 0 :
            
            df = pd.DataFrame(mod_items)                    
            item_adda_after = df[df["title"] == LABEL_METHOD_ADDA_AFTER]
        
            # Exist the LABEL_METHOD_ADDA_AFTER ?
            if len(item_adda_after) == 1:
        
                pos_adda_after = item_adda_after['position'].values[0]

                # Verify if the forum after was create
                if df[df['title'].str.startswith(S_NRO_SESSION + " : IA ->")].empty:

                    # Create discussion topic
                    dt_after = DiscussionTopic(self.course_id, self.access_token)

                    title_discussion_topic_after = \
                        self.template_discussion_topic["after"]["title"].replace(TEMPLATE_SHORT_SESSION,S_NRO_SESSION)
                    
                    res_dt_after = dt_after.create_discussion_topic(title_discussion_topic_after,
                                                                    self.template_discussion_topic["after"]["message"])

                    # Create link to discussion topic in module
                    self.create_discussion_topics_module(mod['id'],res_dt_after['id'], pos_adda_after+1)            
                         
    def configure(self, w_from, w_to, action="R"):
        super().configure(w_from, w_to, action)        
        print("===============> Configure ADDA methodology <================")
        for mod in self.get_modules():
            #print(mod)
            if (mod["name"].startswith(KEY_MOD_1) or mod["name"].startswith(KEY_MOD_2) ) :
                #idx += 1
                nro_week = self.get_nro_week(mod["name"])
                if  w_from <= nro_week <= w_to :
                    print("\n====> [%s] : %s \n"%(mod["position"] , mod["name"]))
                    if action == "C":   self.config_module_course(mod, nro_week)  
                    if action == "D":   self.clean_module_course(mod, nro_week)  
