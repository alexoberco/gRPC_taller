import grpc
from concurrent import futures
import json
import gRPC_pb2
import gRPC_pb2_grpc



def run():
    with grpc.insecure_channel("200.3.152.101:50051") as channel:
        stub = gRPC_pb2_grpc.StudentServiceStub(channel)
        respuesta = "s"
        while(respuesta == "s" or respuesta == "S"):
            print("1. obtener nombre")
            print("2. obtener promedio de notas")
            print("3. obtener grupo")

            rpc_call = input("ingrese la opcion: ")

            respuesta = "s"
        
            if rpc_call == "1":
                id = input("ingrese el id del estudiante: ")
                idRequest = gRPC_pb2.GetNameRequest(id=int(id))
                idreply = stub.GetName(idRequest)
                print(f"El nombre del estudiante con el id {id} es: {idreply.full_name}")
            elif rpc_call == "2":
                student_input = input("ingrese el id o nombre del estudiante: ")
                try:
                    # Intenta convertir a int, si falla, asume que es un nombre
                    student_id = int(student_input)
                    gradeRequest = gRPC_pb2.GetAverageScoreRequest(id=student_id)
                except ValueError:
                    gradeRequest = gRPC_pb2.GetAverageScoreRequest(name=student_input)
                gradeReply = stub.GetAverageScore(gradeRequest)
                print(f"El promedio del estudiante es: {gradeReply.average_score}")
            elif rpc_call == "3":
                id = input("ingrese el id del estudiante: ")
                groupRequest = gRPC_pb2.GetGroupRequest(id=int(id))
                groupReply = stub.GetGroup(groupRequest)
                print(f"El grupo del estudiante es: {groupReply.group}")
            else:
                print("El valor ingresado no está dentro de las opciones, ingrese otro valor\n")
            
            respuesta = input("desea obtener algun otro dato? s para si u otro caracter para no: ")



if __name__ == "__main__":
    run()