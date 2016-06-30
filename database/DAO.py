from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.Readxml import *
import database.settings
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from database import Associations
# import database.Associations
from database.Interruption import Interruption
from database.History_entry import History_entry
from database.Instance import Instance
from database.WED_attribute import WED_attribute
from database.WED_condition import WED_condition
from database.WED_flow import WED_flow 
from database.WED_transition import WED_transition
from database.WED_trigger import WED_trigger
from database.Readxml import Readxml
from database.WED_state import WED_state

# from database.settings import *

class DAO:

    def __init__(self):
        self.engine = create_engine(URL(**database.settings.DATABASE))
        #self.readxml = Readxml('../xml/B1.xml')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()    
        self.readxml = None

    def __del__(self):
        self.session.close_all()
        self.engine

    def set_readxml(self, readxml):
        self.readxml = readxml

    def create_tables(self):
        #Base.metadata.create_all(self.engine)
        WED_attribute.__table__.create(self.engine)
        WED_condition.__table__.create(self.engine)
        WED_transition.__table__.create(self.engine)
        WED_flow.__table__.create(self.engine)
        WED_trigger.__table__.create(self.engine)
        Instance.__table__.create(self.engine)
        #tabelas history e instance será criadas depois da wed_state
        #History_entry.__table__.create(self.engine)
        #Interruption.__table__.create(self.engine)

        #wedState_wedTrigger

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    def insert(self):
        list_attributes = self.readxml.data_wed_attributes()
        for attributes in list_attributes:
            self.session.add(attributes)
            self.session.commit()

        # depois de ler os wed_attributes cria a tabela wed_state, como History tem relacionamento com
        # wed-state, entao cria ele depois do wed_state e Interruption tem relacionamento com
        # History entao cria tbn.
        DAO.create_necessary_tables(self)
        
        list_conditions = self.readxml.data_wed_conditions()
        for condition in list_conditions:
            self.session.add(condition)
            self.session.commit()        

        list_transitions = self.readxml.data_wed_transitions()
        for transitions in list_transitions:
            self.session.add(transitions)
            self.session.commit()
                                
        list_flows = self.readxml.data_wed_flows()
        for flows in list_flows:
            self.session.add(flows)
            self.session.commit()        

        list_trigger = self.readxml.data_wed_trigger()
        for trigger in list_trigger:
            self.session.add(trigger)
            self.session.commit()    

    def create_necessary_tables(self):
        WED_state.__table__.create(self.engine)
        History_entry.__table__.create(self.engine)
        Interruption.__table__.create(self.engine)
        Associations.wedState_wedTrigger.create(self.engine)
  
    def select_condition(self, wed_condition):
        result = self.session.execute(
            "SELECT id FROM wed_condition WHERE name = '" + wed_condition + "'"
        ).fetchone()
        return result

    def select_transition(self, wed_transition):
        result = self.session.execute(
            "SELECT id FROM wed_transition WHERE name = '" + wed_transition + "'"
        ).fetchone()
        return result

    def select_flow(self, wed_flow):
        result = self.session.execute(
            "SELECT id FROM wed_flow WHERE name = '" + wed_flow + "'"
        ).fetchone()
        return result     

    def select_trigger(self):
        return self.session.query(WED_trigger)

    def select_fila(self, trigger_id):
        return self.session.query(Associations.wedState_wedTrigger).filter_by\
                (wed_trigger_id = trigger_id)

    def select_state(self, state_id):
        return self.session.query(WED_state).filter_by(id = state_id)

    def select_condition(self, condition_id):
        return self.session.query(WED_condition).filter_by(id = condition_id)

    def select_wedflow2(self, wedflow_id):
        return self.session.query(WED_flow).filter_by(id=wedflow_id)