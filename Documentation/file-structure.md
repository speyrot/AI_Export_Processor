# Project File Structure

This document provides an overview of the file and directory organization for the **ExportProcessor2** project, encompassing both frontend and backend components, along with documentation and configuration files. Adhering to this structure ensures maintainability, scalability, and ease of navigation for all team members.

## Root Directory: `ExportProcessor2/`

ExportProcessor2/ 
├── backend/ 
├── frontend/ 
├── Documentation/ 
├── .cursorrules 
└── README.md


### Overview

- **backend/**: Contains all backend-related code and configurations.
- **frontend/**: Houses the frontend application built with Next.js and React.
- **Documentation/**: Includes all project documentation files.
- **.cursorrules**: Configuration file for cursor behavior (to be created).
- **README.md**: Provides an introduction and overview of the project.

---

## Backend Directory: `backend/`

backend/ 
├── app/ 
│ ├── api/ 
│ │ ├── endpoints/ 
│ │ │ ├── upload.py 
│ │ │ ├── download.py 
│ │ │ └── auth.py 
│ │ └── init.py 
│ ├── core/ 
│ │ ├── config.py 
│ │ ├── security.py 
│ │ └── init.py 
│ ├── models/ 
│ │ ├── invoice.py 
│ │ └── user.py 
│ ├── services/ 
│ │ ├── processing.py 
│ │ └── storage.py 
│ ├── utils/ 
│ │ └── helpers.py 
│ ├── main.py 
│ └── init.py 
├── tests/ 
│ ├── unit/ 
│ └── integration/ 
├── requirements.txt 
├── Dockerfile 
├── docker-compose.yml 
└── README.md


### Directory Breakdown

- **app/**: Core application code.
  - **api/**: Contains API route definitions.
    - **endpoints/**: Individual API endpoints handling specific functionalities.
      - `upload.py`: Handles invoice file uploads.
      - `download.py`: Manages invoice file downloads.
      - `auth.py`: Manages authentication processes.
    - `__init__.py`: Initializes the API module.
  - **core/**: Core configurations and security settings.
    - `config.py`: Configuration settings for the application.
    - `security.py`: Security-related configurations and utilities.
    - `__init__.py`: Initializes the core module.
  - **models/**: Database models representing data structures.
    - `invoice.py`: Defines the Invoice model.
    - `user.py`: Defines the User model.
  - **services/**: Business logic and service integrations.
    - `processing.py`: Handles data preprocessing and transformation.
    - `storage.py`: Manages interactions with Supabase Storage.
  - **utils/**: Utility functions and helpers.
    - `helpers.py`: Contains helper functions used across the application.
  - `main.py`: Entry point for the FastAPI application.
  - `__init__.py`: Initializes the app module.
  
- **tests/**: Testing suites.
  - **unit/**: Unit tests for individual components and functions.
  - **integration/**: Integration tests ensuring components work together seamlessly.
  
- **requirements.txt**: Lists Python dependencies required for the backend.
  
- **Dockerfile**: Defines the Docker image for containerizing the backend application.
  
- **docker-compose.yml**: Configures Docker services for local development and testing.
  
- **README.md**: Provides an overview and setup instructions for the backend.

---

## Frontend Directory: `frontend/`

frontend/ 
├── components/ 
│ ├── UploadForm/ 
│ ├── DownloadLink/ 
│ ├── Auth/ 
│ └── ... 
├── pages/ 
│ ├── index.tsx 
│ ├── _app.tsx 
│ ├── login.tsx 
│ ├── signup.tsx 
│ └── ... 
├── styles/ 
│ ├── globals.css 
│ └── ... 
├── hooks/ 
│ └── useFetch.ts 
├── utils/ 
│ └── api.ts 
├── public/ 
│ └── assets/ 
├── tests/ 
│ └── components/ 
├── types/ 
│ └── index.d.ts 
├── supabaseClient.ts 
├── next.config.js 
├── tsconfig.json 
└── package.json


### Directory Breakdown

- **components/**: Reusable UI components.
  - **UploadForm/**: Component for uploading invoice files.
  - **DownloadLink/**: Component for downloading processed files.
  - **Auth/**: Components related to authentication (e.g., login, signup).
  - `...`: Placeholder for additional components as needed.
  
- **pages/**: Next.js pages handling routing and rendering.
  - `index.tsx`: Home page.
  - `_app.tsx`: Custom App component for initializing pages.
  - `login.tsx`: Login page.
  - `signup.tsx`: Signup page.
  - `...`: Placeholder for additional pages.
  
- **styles/**: Styling files.
  - `globals.css`: Global CSS styles leveraging Bootstrap.
  - `...`: Placeholder for additional styling files.
  
- **hooks/**: Custom React hooks.
  - `useFetch.ts`: Hook for fetching data from APIs.
  
- **utils/**: Utility functions and helpers.
  - `api.ts`: Configures Axios and Supabase client interactions.
  
- **public/**: Static assets served by the frontend.
  - **assets/**: Images, fonts, and other static files.
  
- **tests/**: Testing suites for frontend components.
  - **components/**: Tests for individual UI components.
  
- **types/**: TypeScript type definitions.
  - `index.d.ts`: Global type declarations.
  
- `supabaseClient.ts`: Initializes and configures the Supabase client.
  
- `next.config.js`: Next.js configuration file.
  
- `tsconfig.json`: TypeScript configuration file.
  
- `package.json`: Lists frontend dependencies and scripts.

---

## Documentation Directory: `Documentation/`

Documentation/ 
├── prd.md 
├── tech-stack.md 
├── app-flow.md 
├── frontend-guidelines.md 
├── backend-guidelines.md 
└── file-structure.md


### Directory Breakdown

- **prd.md**: Product Requirements Document detailing project objectives, inputs, outputs, and requirements.
  
- **tech-stack.md**: Detailed description of the technology stack, including cloud services, frameworks, and libraries used.
  
- **app-flow.md**: Comprehensive overview of the application workflow, including data flow and security considerations.
  
- **frontend-guidelines.md**: Guidelines for frontend development, outlining coding standards, best practices, and architectural decisions.
  
- **backend-guidelines.md**: Guidelines for backend development, covering coding standards, architecture, and integration with Supabase.
  
- **file-structure.md**: (This current document) Details the organization and purpose of all project files and directories.

---

## Configuration Files

- **.cursorrules**: Configuration file to define cursor behaviors across the application. 
  
- **README.md**: Provides an overview and instructions for the entire project, including setup, usage, and contribution guidelines.

---

## Summary

This **file structure** is designed to maintain simplicity and clarity, ensuring that both frontend and backend components are well-organized and easy to navigate. By leveraging **Supabase** for backend services and **Bootstrap** for frontend styling, the project remains efficient and maintainable, suitable for an internal application with a limited user base.

- **Backend** focuses on API endpoints, services, and models, integrating seamlessly with Supabase for authentication, storage, and database management.
  
- **Frontend** utilizes Next.js and React with Bootstrap for consistent and responsive UI, interacting with the backend and Supabase through well-defined utilities and hooks.
  
- **Documentation** ensures that all aspects of the project are well-documented, facilitating onboarding and ongoing maintenance.