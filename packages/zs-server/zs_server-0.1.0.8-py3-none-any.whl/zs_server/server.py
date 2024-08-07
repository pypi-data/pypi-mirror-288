#!/usr/bin/env python

import asyncio
import websockets
import subprocess
import copy
from multiprocessing import Process as mp
from threading import Thread
import hashlib
import json
import time
from collections import deque
from pathlib import Path
import os, psutil, argparse
from getpass import getpass

"""
{'websocket': {'hashproc':{

                            },
                'hashproc':{
                
                            }
                }
    }
"""
class Proc:
    def __init__(self):
        self.__proc = dict()
        self.__taskprocid = dict()
        self.__taskmgmt = deque()

        
    def __execute(self, websocket, hashproc, command, cwd=None):
        print(f'Executing command \'{command}\'')
        #await websocket.send("Executed command with id x")
        # exit_code, output = subprocess.getstatusoutput(cmd=command)
        try:
            self.__proc[websocket][hashproc]['subproc'] = subprocess.Popen(command, stdout=subprocess.PIPE, stderr = subprocess.PIPE,shell=True, cwd = cwd if cwd else None)
            # p = subprocess.run(command.split(), capture_output=True, shell=True)
            communicate = self.__proc[websocket][hashproc]['subproc'].communicate()
            output = communicate[0].decode('utf-8').strip()
            exit_code=0
            if not len(output):
                exit_code = "-1"
                output = communicate[1].decode('utf-8').strip()
            if self.__proc.get(websocket):
                self.__proc[websocket][hashproc]['output'] = output
                self.__proc[websocket][hashproc]['exit_code'] = exit_code
                self.__proc[websocket][hashproc]['status'] = True
        except Exception as E:
            if self.__proc.get(websocket):
                self.__proc[websocket][hashproc]['output'] = f"{E}"
                self.__proc[websocket][hashproc]['exit_code'] = "-1"
                self.__proc[websocket][hashproc]['status'] = True
        #if self.proc.get()
    def run_command(self,command, websocket, cwd=None):
        # if self.get
        #await websocket.send("Executed command with id x")
        hashproc = hashlib.sha384(command.strip().encode('utf-8')).hexdigest()
        response =""
        if ";" in command:
            command, cwd = command.split(";")
            cwd= Path(cwd)
            if not cwd.exists():
                response = {'status': False,'id': hashproc, 'message':f"Path - {cwd} does not exist"}
                response = json.dumps(response)
                return response
        if self.__proc.get(websocket).get(hashproc) is None or (self.__proc.get(websocket).get(hashproc) and self.__proc.get(websocket).get(hashproc).get('status')):
            if (self.__proc.get(websocket).get(hashproc) and self.__proc.get(websocket).get(hashproc).get('status')):
                self.__proc[websocket].pop(hashproc)
            self.__proc[websocket][hashproc] = dict()
            proc = Thread(target=self.__execute,args=(websocket, hashproc, command, cwd))
            proc.start()
            self.__proc[websocket][hashproc]['proc'] = proc
            print(f'Executed command\'s Thread ID: {proc.native_id}\n')
            
            response = {'status': True,'id': hashproc, 'message':f"Successfully ran command - {command}. Please poll to get status of this command using ID attribute"}
            response = json.dumps(response)
        else:
            print("Execute command is already in execution")
            response = {'status': False,'id': hashproc, 'message':f"Cannot run command - {command} as previous state of this command is still in execution"}
            response = json.dumps(response)
        return response
        
        
    def insert_websocket(self, websocket):
        if self.__proc.get(websocket) is None:
            self.__proc[websocket] = dict()
            # self.__proc[websocket]['timestamp'] = int(time.time())

    def terminate(self,procid):
        process = psutil.Process(pid=procid)
        for proc in process.children(recursive=True):
            proc.terminate()
            print(f"killed proc {proc.pid}")
        process.terminate()

    def remove_websocket(self, websocket):
        if self.__proc.get(websocket) is not None:
            taskhashproc = self.__proc[websocket].get('taskhashproc')
            if taskhashproc:
                self.__proc[websocket].pop('taskhashproc')
                if self.__taskprocid.get(taskhashproc):
                    self.__taskprocid[taskhashproc]['status'] = True
                    self.__taskprocid[taskhashproc]['exit_code'] = "1"
                    self.__taskprocid[taskhashproc]['output']= f"Task could not finish due to aborted connection from {websocket.remote_address[0]}"

            for hashproc in list(self.__proc.get(websocket).keys()):
                ret_data= self.__proc.get(websocket).get(hashproc).get('status')
                if not ret_data:
                    subproc = self.__proc.get(websocket).get(hashproc).get('subproc')
                    self.terminate(procid=subproc.pid)
                    # print(self.__proc.get(websocket).get(hashproc).get('output'))
                
            self.__proc.pop(websocket, None)

    def get_all_clients(self):
        return self.__proc

    def keep_alive(self):
        print("Keeeping connection alive using ping-pong method")
        return json.dumps({'status': True, 'message':"Keeping the connection alive"})

    def pull_proc_info(self,websocket, hashproc):
        ret_data = dict()
        if self.__proc.get(websocket).get(hashproc):
            ret_data['output'] = self.__proc.get(websocket).get(hashproc).get('output')
            ret_data['exit_code'] = self.__proc.get(websocket).get(hashproc).get('exit_code')
            ret_data['status'] = self.__proc.get(websocket).get(hashproc).get('status')
            if ret_data['status'] or ret_data['exit_code'] is not None:
                self.__proc.get(websocket).pop(hashproc)
            return json.dumps(ret_data)
        
        if  self.__taskprocid.get(hashproc):
            ret_data['output']= self.__taskprocid[hashproc]['output']
            ret_data['exit_code'] = self.__taskprocid[hashproc]['exit_code']
            ret_data['status'] = self.__taskprocid[hashproc]['status']
            if ret_data['status'] or ret_data['exit_code'] is not None:
                self.__taskprocid.pop(hashproc)
                # self.__proc[websocket].pop('taskhashproc')
            return json.dumps(ret_data)
        
        ret_data['status'] = False
        ret_data['message'] = f"Process ID - {hashproc} is not active"
        ret_data['exit_code']= "-2"
        ret_data['output'] = None
        return json.dumps(ret_data)
    
    def add_task(self,websocket, task):
        if websocket.remote_address[0] == "127.0.0.1":
            hashproc = hashlib.sha384(task.encode('utf-8')).hexdigest()
            task =  json.loads(task)
            self.__taskprocid[hashproc] = dict()
            self.__taskprocid[hashproc]['task'] = task
            self.__taskprocid[hashproc]['status'] = False
            self.__taskprocid[hashproc]['exit_code']= None
            self.__taskprocid[hashproc]['output']= None
            # print(self.__taskprocid[hashproc])
            self.__taskmgmt.append(hashproc)
            return json.dumps({"status":True, "message":"Successfully added task to pending queue", "id": hashproc})
        return json.dumps({"status":False, "message": "Permission denied. Task can only be added by local-client."})
    
    def get_first_pending_task(self, websocket,hashproc=None):
        if websocket.remote_address[0] == "127.0.0.1":
            return json.dumps({"status": False, "message": f"Localhost client does not have permission to execute Tasks"})
        if not len(self.__taskmgmt) and hashproc is None:
            return json.dumps({"status": False, "message": "No Pending task in queue"})
        if hashproc:
            if self.__taskprocid.get(hashproc) is not None: 
                # taskop = self.__taskprocid.get(hashproc)
                taskop = self.__taskprocid.get(hashproc).get('task')
                # self.__taskprocid[hashproc]['websocket'] = websocket.remote_address[0]
                self.__proc[websocket]['taskhashproc'] = hashproc
                return json.dumps({"status":True, "id": hashproc, "message": f"Successfully fetched pending task with id - {hashproc}", "output":taskop})
            return json.dumps({"status": False, "message": f"No pending task in queue with id {hashproc}"})
        return json.dumps({"status": True, "message":"Successfully fetched the first pending task.", "id": self.__taskmgmt.popleft()})

    def set_first_pending_task(self, websocket, data):
        data = json.loads(data)
        if data.get('id') and self.__proc[websocket]['taskhashproc'] == data.get('id') and self.__taskprocid.get(data.get('id')):
            self.__taskprocid[data.get('id')]['output'] = data.get('output')
            self.__taskprocid[data.get('id')]['exit_code'] = data.get('exit_code')
            self.__taskprocid[data.get('id')]['status'] = data.get('status')
            return json.dumps({"status":True, "message": f"Successfully updated the status of pending task - {data.get('id')}"})
        
        return json.dumps({"status": False, "message": f"Cannot find task id - {data.get('id')}"})
            
WorkerProcess = Proc()
async def server(websocket):
    WorkerProcess.insert_websocket(websocket)
    # while True:
    try:
        # try:
        async for command in websocket:
            # command = await websocket.recv()
            print(command)
            print(f"Client lenght = {len(WorkerProcess.get_all_clients())}")
            print(websocket.remote_address)
            if "close" in command:
                WorkerProcess.remove_websocket(websocket)
                print(f"Client lenght = {len(WorkerProcess.get_all_clients())}")
                response = json.dumps({"status": True, "message": "Removed connection from active client list"})
                await websocket.send(response)
                
                continue

            if "keep-alive" in command:
                response = WorkerProcess.keep_alive()
                await websocket.send(response)
                continue
            if "pull_proc_info" in command:

                response= WorkerProcess.pull_proc_info(websocket=websocket, hashproc=command.split("=")[-1])
                await websocket.send(response)
                continue
            
            if "add_task" in command:
                response = WorkerProcess.add_task(websocket=websocket,task= command.split("=")[-1])
                await websocket.send(response)
                continue
            
            if "fetch_pending_id" in command:
                response = None
                if len(command.split("=")) > 1:
                    response = WorkerProcess.get_first_pending_task(websocket = websocket, hashproc = command.split("=")[-1])
                else: response = WorkerProcess.get_first_pending_task(websocket=websocket)
                await websocket.send(response)
                continue
            # print(f'Executing command \'{command}\'')
            if "update_pending_id" in command:
                response = WorkerProcess.set_first_pending_task(websocket=websocket, data= command.split("=")[-1])
                await websocket.send(response)
                continue
            response = WorkerProcess.run_command(command=command, websocket=websocket)
            # pid = WorkerProcess.run_command(command, hashproc)
            #await websocket.send("Executed command with id x")
            # proc = mp(target=subprocess.getstatusoutput,args=(command,))
            # print(proc.pid)
            # print(proc.pid)
            # proc.start()
            # proc.
            # thread.pid
            # (exit_code, output) = subprocess.getstatusoutput(command)
            # if len(output.strip()) > 0:
            #     print(output, flush=True)
            #     print("\n")
            # print(f'Executed command\'s process ID: {pid}\n')
            #proc.join()
            #yield websocket.send(str(exit_code))
            await websocket.send(response)
    
    except websockets.ConnectionClosed as E:
        #print(E)
        #print("SOMETHING")
        #clients.remove(websocket)
        WorkerProcess.remove_websocket(websocket)
        # break
       
async def start_server(user, password):
    
    async with websockets.serve(server, port= 1463,create_protocol=websockets.basic_auth_protocol_factory(
        realm="WorkerAgent",
        credentials=(user, password)
    )):
        await asyncio.Future()  # run forever
    # print("Something")
    # p = Thread(target=websockets.serve, args=(server,1463))
    # p.start()
    # print("some")
    # await asyncio.Future()
    
    # serv =websockets.serve(server, 1463)
    # asyncio.get_event_loop().run_until_complete(serv)
    # asyncio.get_event_loop().run_forever()

def main():
    user = getpass(prompt="Windows User Name: ")
    password = getpass()
    print("Server Started ...\n\n")
    asyncio.run(start_server(user, password))
if __name__ == "__main__":
    main()