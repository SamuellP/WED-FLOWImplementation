from database import *
import schedule
from datetime import datetime
import time


# transition
    # bloqueia o estado atual na instancia.
    # cria um novo estado
    # atualiza estado atual no Instance e libera o bloqueio
    # atualiza o history_entry (monitor passa a linha do history)
    # Inserir o novo estado nas filas

def avalia_trigger(condition, state, dao):
    dao.select_condition(condition.id)

    

def make_func(t, dao):
    def _function():
        '''
        recuper a fila da trigger X
        Para cada wed_state da fila avalia a condition da trigger
        se true: dispara a transition
        '''

        
        fila = dao.select_fila(t.id).filter_by(status = "started").all()
        
        # update status para processando (feito)
        for i in fila:
            fila.status = "processing"
        dao.session.commit()


        # status = Column(String(50))
        # create_at = Column (DateTime)
        # completed_at =  Column (DateTime)
        # instance_id = Column(Integer, ForeignKey('instance.id'))
        # instance = relationship("Instance", back_populates="history_entry")

        # initial_state_id = Column(Integer, ForeignKey('wed_state.id'))
        # current_state_id = Column(Integer, ForeignKey('wed_state.id'))

        # initial_state = relationship("WED_state", foreign_keys = [initial_state_id])
        # current_state = relationship("WED_state", foreign_keys = [current_state_id])


        # final_state_id = Column(Integer, ForeignKey('wed_state.id'))
        # final_state = relationship("WED_state", foreign_keys = [final_state_id])

      
        # interruption = relationship("Interruption", uselist=False, back_populates="history_entry")
        # wed_transition_id = Column(Integer, ForeignKey('wed_transition.id'))
        # wed_transition = relationship("WED_transition", back_populates="history_entry")

        
        for i in fila:
            r = avalia_trigger(t.condition, dao.select_state(fila.wed_state_id), dao)
            if(r == True):
                history_entry = History_entry()
                pass
                # Criar a entrada no history_entry
                # dispara transition (a transition atualiza o history_entry)

            # update para processado (finish)
        print('t_'+str(t.id) + ': Funcionou')
    return _function


    # status = Column(String(50))
    # create_at = Column (DateTime)
    # finalized_at =  Column (DateTime)
    # wed_flow_id = Column(Integer, ForeignKey('wed_flow.id'))
if __name__ == '__main__':
    dao = DAO()
    # wedflow = dao.select_wedflow2(1)
    # ins = Instance(status = 'started', create_at = datetime.now(), wed_flow_id = wedflow[0])
    # dao.session.add(ins)
    # dao.session.commit()

    result = dao.select_trigger()
    for i in result:
        job = make_func(i, dao)
        schedule.every(i.id).seconds.do(job)


    while True:
        schedule.run_pending()
        time.sleep(1)

