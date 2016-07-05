from database import *
import schedule
from datetime import datetime
import time
import _thread


# transition
    # bloqueia o estado atual na instancia.
    # cria um novo estado
    # atualiza estado atual no Instance e libera o bloqueio
    # atualiza o history_entry (monitor passa a linha do history)
    # Inserir o novo estado nas filas

def avalia_trigger(condition, state, dao):
    pass

def make_func(trigger, dao):
    def _function():
        '''
            recuper a fila da trigger X
            Para cada wed_state da fila avalia a condition da trigger
            se true: dispara a transition
        '''
        fila_wedStates_wedTriggers = dao.select_fila(trigger.id)
        
        # update status para processando (feito)
        for i in fila_wedStates_wedTriggers:
            i.status = "processing"
        dao.session.commit()

        for i in fila_wedStates_wedTriggers:
            result = avalia_trigger(trigger.wed_condition, dao.select_state(i.wed_state_id), dao)
            if(result == True):
                # Criar a entrada no history_entry
                instance = dao.select_instance(dao.select_state(i.wed_state_id)[0])[0]
                history_entry = History_entry(create_at = datetime.now(), instance_id = instance.id, \
                    initial_state_id = i.wed_state_id, wed_transition_id = i.wed_transition_id) # FALTA O INTERRUPTION
                history_entry.add()
                dao.session.commit()
                
                transition = dao.select_transition(i.wed_transition_id)

                # Carrega a classe da transition
                package = __import__("transitions")
                module = getattr(package, transition.name)
                class_ = getattr(module, transition.name)

                # cria e inicia a thread da transition
                try:
                   _thread.start_new_thread(class_.run, (dao, instance, history_entry))
                   # _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
                except:
                   print ("Error: unable to start thread")


        # update para processado (finish)
        for i in fila_wedStates_wedTriggers:
            i.status = "finish"
        dao.session.commit()
        
        print('trigger_'+str(trigger.id) + ': Funcionou')

    return _function





if __name__ == '__main__':
    dao = DAO()

    result = dao.select_trigger()
    for i in result:
        job = make_func(i, dao)
        schedule.every(i.period).seconds.do(job)


    while True:
        schedule.run_pending()
        time.sleep(1)

