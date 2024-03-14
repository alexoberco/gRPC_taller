import grpc
from concurrent import futures
import json

import gRPC_pb2
import gRPC_pb2_grpc

# Cargar los datos de los estudiantes desde el archivo JSON en una variable
with open('data/students.json') as f:
    student_list = json.load(f)

# Convertir la lista de estudiantes en un diccionario para una búsqueda eficiente por ID
students_by_id = {student['ID']: student for student in student_list}

class StudentService(gRPC_pb2_grpc.StudentServiceServicer):

    def GetName(self, request, context):
        # Buscar el estudiante por ID y devolver el nombre completo
        student = students_by_id.get(request.id)
        if student is not None:
            return gRPC_pb2.GetNameResponse(full_name=student['Nombre'])
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Student with ID={} not found'.format(request.id))

    def GetAverageScore(self, request, context):
        # Buscar el estudiante por nombre o ID y devolver el promedio de notas
        student = None
        if request.HasField('id'):
            student = students_by_id.get(request.id)
        elif request.HasField('name'):
            student = next((s for s in student_list if s['Nombre'] == request.name), None)

        if student is not None:
            average_score = (student['Taller 1'] + student['Taller 2']) / 2
            return gRPC_pb2.GetAverageScoreResponse(average_score=average_score)
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Student not found')

    def GetGroup(self, request, context):
        # Buscar el estudiante por ID y devolver el grupo de trabajo
        student = students_by_id.get(request.id)
        if student is not None:
            return gRPC_pb2.GetGroupResponse(group=student['Grupo'])
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, 'Student with ID={} not found'.format(request.id))

# Función para correr el servidor
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gRPC_pb2_grpc.add_StudentServiceServicer_to_server(StudentService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
