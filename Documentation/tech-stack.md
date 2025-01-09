# Technology Stack

## Overview
The AI-Based Automated Invoice Processing Workflow leverages a combination of cloud services, machine learning APIs, web technologies, and data processing libraries to achieve its objectives efficiently and securely. The updated technology stack integrates **Supabase** for backend services, enhancing scalability and maintainability while simplifying infrastructure management.

## Components

### Cloud Hosting & Backend Services
- **Supabase:**
  - **Database:** PostgreSQL managed by Supabase for storing user data, invoice metadata, and processed file references.
  - **Authentication:** Supabase Auth for managing user authentication and authorization.
  - **Storage:** Supabase Storage for storing uploaded and processed invoice files securely.
- **AWS (Amazon Web Services):**
  - **EC2 (Elastic Compute Cloud):** Hosting the backend and frontend web applications.
  - **CloudWatch:** Monitoring and logging application performance and health.
  - **IAM (Identity and Access Management):** Managing access control and permissions for AWS services.

### Machine Learning
- **OpenAI GPT-3.5 Turbo or GPT-4:**
  - **Usage:** Leveraged for intelligent data transformation, column mapping, and handling variability in invoice formats through API integration.
  - **Integration:** Accessed via OpenAI API keys, enabling prompt engineering to tailor responses for accurate invoice processing.

### Web Application
- **Frontend:**
  - **Next.js:** A React-based framework used for building the user interface, providing server-side rendering, and optimizing performance.
  - **React:** Core library for building interactive and dynamic UI components.

- **Backend:**
  - **FastAPI:** A high-performance Python framework for building robust and scalable APIs, handling file uploads, processing requests, and interacting with OpenAI’s APIs.

### Deployment
- **AWS EC2:** Primary deployment platform for hosting both frontend and backend applications, ensuring scalability and reliability.
- **AWS Elastic Beanstalk (Optional):** An alternative for managing deployments with reduced operational overhead, providing automatic scaling and load balancing.

### Security
- **HTTPS:** Ensures secure data transmission between clients and the server, protecting sensitive invoice data during upload and download processes.
- **IAM Roles:** Manages fine-grained access control and permissions for AWS services, ensuring that only authorized components can interact with each other.
- **Supabase Security:** Supabase’s built-in security features for managing database access, authentication, and storage permissions.
- **Environment Variables:** Securely manages sensitive information such as API keys and database credentials, preventing exposure in the codebase.

### Data Processing
- **Python Libraries:**
  - **pandas:** Utilized for data manipulation, cleaning, and transformation of invoice data to ensure consistency and adherence to export specifications.
  - **fuzzywuzzy:** Employed for fuzzy string matching to handle variations in column headers, facilitating accurate data mapping and transformation.

### Additional Tools and Libraries
- **Axios:** Used in the frontend for making HTTP requests to the backend APIs, enabling efficient data fetching and submission.
- **Formik and Yup:** Implemented for form handling and validation in the frontend, ensuring robust user input management.
- **Docker (Optional):** Containerizes the backend and frontend applications, promoting consistent environments across development, testing, and production.
- **GitHub Actions (Optional):** Integrated for Continuous Integration/Continuous Deployment (CI/CD) pipelines, automating testing and deployment workflows.

## Integration Points

- **OpenAI API:** Central to the AI-driven data transformation process, requiring secure and efficient API communication.
- **Supabase Services:**
  - **Database:** Utilized for storing user information, invoice metadata, and references to stored files.
  - **Authentication:** Manages user sign-in, sign-up, and session handling securely.
  - **Storage:** Handles the storage and retrieval of uploaded and processed invoice files.
- **AWS Services:** Utilized primarily for hosting the web application on EC2 and monitoring with CloudWatch.
- **Frontend and Backend Communication:** Managed via RESTful APIs built with FastAPI, facilitating smooth data flow and user interactions.

## Security Considerations

- **Data Encryption:** All data in transit is encrypted using HTTPS, and sensitive data stored in S3 is encrypted at rest.
- **Access Control:** Strict IAM policies are enforced to limit access to AWS resources, ensuring that only necessary services and personnel have the required permissions.
- **API Key Management:** OpenAI API keys are stored securely using environment variables and are never exposed in the frontend codebase.

## Scalability and Performance

- **Scalable Infrastructure:** AWS EC2 instances can be scaled horizontally to handle increased load as the number of users or volume of invoices grows.
- **Efficient Data Processing:** Leveraging pandas and fuzzywuzzy ensures fast and reliable data manipulation, while OpenAI’s optimized models provide quick and accurate transformations.
- **Load Balancing:** (If using Elastic Beanstalk) Automatically distributes incoming traffic across multiple instances to ensure high availability and reliability.

## Development and Deployment Workflow

1. **Development Environment:**
   - Use Docker for creating consistent development environments (if opted).
   - Employ TypeScript for frontend development to enhance type safety and developer experience.
   - Utilize virtual environments for Python to manage dependencies effectively.

2. **Version Control:**
   - Git is used for source code management, with repositories hosted on platforms like GitHub or GitLab.
   - Follow Git branching strategies (e.g., GitFlow) to manage feature development, releases, and hotfixes.

3. **Continuous Integration/Continuous Deployment (CI/CD):**
   - Implement automated testing using GitHub Actions or similar tools to ensure code quality.
   - Automate deployment to AWS EC2 or Elastic Beanstalk upon successful builds and tests, minimizing manual intervention.