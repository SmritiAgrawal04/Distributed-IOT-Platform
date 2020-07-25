import sqlite3 


def prep_serverInfo(statistics):
    # print ("statistics= ",statistics)
    connection = sqlite3.connect("Server_DB.sqlite3") 
    crsr = connection.cursor() 

    for key, stats in statistics.items():
        try:
            task= (stats['server_id'], stats['server_ip'], int(stats['server_port']), float(stats['cpu_utilization']), float(stats['used_memory']), float(stats['free_memory']))
            sql_command= '''INSERT INTO server_info (server_id, server_ip, server_port, cpu_utilization, used_memory, free_memory) VALUES (?, ?, ?, ?, ?, ?)'''
            crsr.execute(sql_command, task)
            connection.commit()
            # print ("Insertion Done in LB")
        except:
            task= (float(stats['cpu_utilization']), float(stats['used_memory']), float(stats['free_memory']), stats['server_id'])
            sql_command= '''UPDATE server_info SET cpu_utilization= ?, used_memory= ?, free_memory= ? WHERE server_id= ?'''
            crsr.execute(sql_command, task) 
            connection.commit()
            # print ("Updation Done")
        # crsr.close()

def get_server(cpu_requirement, memory_requirement):
    connection = sqlite3.connect("Server_DB.sqlite3") 
    crsr = connection.cursor() 

    task= (cpu_requirement, memory_requirement)
    sql_command= '''SELECT server_id, server_ip,server_port, MIN(cpu_utilization),used_memory, MIN(free_memory) FROM server_info WHERE cpu_utilization> ? AND free_memory>=? ;'''
    crsr.execute(sql_command,task)
    server = crsr.fetchall()
    # print ("$$$$$$$", server, "$$$$$$$")
    return server