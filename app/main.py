from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers.router import router as main_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # List of allowed origins
    allow_credentials=False,           # Allow cookies, authorization headers, etc.
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)


async def not_found(request, exc):
    return JSONResponse({"message":"Route Not Found"}, status_code=request.status_code)


@app.get("/")
def health():
    return {"message":"Welcome to local Pune Farmer Market Rates API"}

@app.get("/health")
def health():
    return {"message":"Health OK"}

@app.get("/docker")
def health():
    return {"code":''' # Use an Ubuntu base image
        FROM ubuntu:latest

        # Install OpenSSH Server
        RUN apt-get update && apt-get install -y openssh-server

        # Create SSH directory and set up password authentication
        RUN mkdir /var/run/sshd && echo 'root:rootpassword' | chpasswd

        # Allow root login and disable PAM restrictions
        RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
            && sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

        # Expose SSH Port
        EXPOSE 22

        # Start SSH Server
        CMD ["/usr/sbin/sshd", "-D"]


        # docker build -t ssh-server .
        # docker network create mynetwork
        # docker run -d --name ssh-server --network mynetwork ssh-server
        # docker exec -it ssh-server bash
        # scp <present_path> <from_where_to_copy_path> --> scp root@ssh-server:/home/vm1.txt /home/from_vm1.txt'''}

        
            
app.include_router(main_router, prefix="/rates", tags=["Rates"])