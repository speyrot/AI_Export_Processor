# Application Flow

## Overview
The AI-Based Automated Invoice Processing Workflow is designed to seamlessly transform client-provided Excel invoices into a standardized `.xls` format required by the export department. This process leverages advanced AI capabilities, robust data processing techniques, and secure cloud infrastructure to ensure accuracy, efficiency, and scalability.

## Workflow Diagram

```mermaid
graph TD
    A[User Uploads Invoice] --> B[Web Interface (Next.js)]
    B --> C[Backend API (FastAPI)]
    C --> D[Data Preprocessing (pandas, fuzzywuzzy)]
    D --> E[AI Model Processing (OpenAI GPT-4)]
    E --> F[Data Transformation]
    F --> G[Generate Standardized .xls File]
    G --> H[Store Processed File (Supabase Storage)]
    H --> I[Provide Download Link to User]
    C --> J[Logging & Monitoring (AWS CloudWatch)]
    C --> K[Error Handling Module]

## Detailed Workflow Steps

1. **User Uploads Invoice**
    - **Action:** Users from the export department upload Excel invoice files through the web interface.
    - **Interface:** A user-friendly upload form built with Next.js facilitates file selection and submission.
    - **Validation:** Frontend performs initial validations (e.g., file type, size) before submission.

2. **Web Interface (Next.js)**
    - **Responsiveness:** Ensures the application is accessible and functional across various devices and screen sizes.
    - **User Feedback:** Displays real-time feedback such as upload progress indicators, success messages, and error notifications.
    - **API Interaction:** Utilizes Axios to send the uploaded file to the backend API securely.

3. **Backend API (FastAPI)**
    - **File Reception:** Receives the uploaded Excel file from the frontend.
    - **Authentication & Authorization:** Utilizes **Supabase Auth** to verify user permissions and ensure secure access.
    - **Task Initiation:** Triggers the data preprocessing workflow upon successful validation.

4. **Data Preprocessing (pandas, fuzzywuzzy)**
    - **Data Cleaning:**
        - **pandas:** Reads and cleans the Excel data, handling missing values, and normalizing data formats.
        - **fuzzywuzzy:** Performs fuzzy string matching to standardize column headers, accommodating variations (e.g., "Product Code" vs. "Style Code").
    - **Data Structuring:** Organizes data into a consistent structure suitable for AI processing and transformation.

5. **AI Model Processing (OpenAI GPT-4)**
    - **API Integration:** Sends preprocessed data to OpenAI’s GPT-4 via secure API calls.
    - **Prompt Engineering:** Crafts specific prompts to guide the AI in accurately mapping and transforming invoice data according to export specifications.
    - **Response Handling:** Receives and processes the AI-generated transformations, ensuring they meet the required standards.

6. **Data Transformation**
    - **Data Mapping:** Aligns AI-processed data with the export department’s standardized `.xls` format.
    - **Consistency Checks:** Ensures data types are consistent and formats are standardized (values instead of formulas).
    - **Error Correction:** Identifies and rectifies any discrepancies or anomalies in the transformed data.

7. **Generate Standardized `.xls` File**
    - **File Creation:** Utilizes Python libraries (e.g., `openpyxl`) to generate the final standardized `.xls` file.
    - **Formatting:** Applies necessary formatting to ensure the file meets all export department requirements.
    - **Quality Assurance:** Performs automated checks to verify the integrity and accuracy of the generated file.

8. **Store Processed File (Supabase Storage)**
    - **Secure Storage:** Uploads the standardized `.xls` file to **Supabase Storage**, ensuring secure and reliable storage.
    - **Organization:** Categorizes files by client and date for easy retrieval and management.
    - **Access Control:** Implements strict Supabase storage policies to control access to stored files.

9. **Provide Download Link to User**
    - **Link Generation:** Creates a secure, time-limited download link for the processed `.xls` file stored in Supabase.
    - **Notification:** Sends the download link back to the user through the web interface, allowing them to retrieve the processed file.
    - **User Interaction:** Users can download the file directly from the web interface with a single click.

10. **Logging & Monitoring (AWS CloudWatch & Supabase Logs)**
    - **Activity Logging:** Records all processing activities, including file uploads, API interactions, and file downloads, using **AWS CloudWatch** and **Supabase’s built-in logging**.
    - **Performance Metrics:** Monitors key performance indicators such as processing time, error rates, and system load.
    - **Alerting:** Configures alerts for critical issues (e.g., failed processing, high error rates) to enable prompt responses.

11. **Error Handling Module**
    - **Detection:** Identifies errors at each stage of the workflow, from file upload to data transformation.
    - **Reporting:** Logs errors with detailed information for troubleshooting and analysis using AWS CloudWatch and Supabase logs.
    - **User Notifications:** Provides clear and actionable error messages to users, guiding them on next steps (e.g., retry upload, contact support).
    - **Recovery:** Implements fallback mechanisms to handle transient issues, such as retrying API calls or restoring from backups.

## Integration Points

OpenAI API
  - Role: Central to AI-driven data transformation and column mapping.
  - Interaction: Securely accessed via API keys, facilitating prompt-based data processing tailored to specific invoice formats.
  - Dependencies: Requires stable internet connectivity and reliable API key management to ensure uninterrupted service.

AWS Services
  - EC2: Hosts both frontend and backend applications, providing scalable compute resources.
  - S3: Acts as the primary storage solution for both uploaded and processed invoice files.
  - CloudWatch: Monitors application performance and logs critical events for maintenance and troubleshooting.
  - IAM: Ensures secure access control across all AWS services, adhering to the principle of least privilege.

Frontend and Backend Communication
  - Protocol: RESTful APIs built with FastAPI facilitate communication between the Next.js frontend and the backend services.
  - Data Flow: Secure transmission of files and data, leveraging HTTPS to protect against interception and tampering.

## Error Handling

Types of Errors
- Client-Side Errors:
  - Invalid file formats or sizes.
  - Network connectivity issues during file upload.
  - User authentication failures.
- Server-Side Errors:
  - Failures in data preprocessing (e.g., corrupted files).
  - API call failures to OpenAI (e.g., rate limits, downtime).
  - Data transformation inaccuracies or inconsistencies.
  - Storage issues in AWS S3.

Error Mitigation Strategies
- Retry Mechanisms: Automatically retry failed API calls to OpenAI with exponential backoff.
- Fallback Procedures: Provide alternative workflows or manual intervention options when critical failures occur.
- Comprehensive Logging: Capture detailed error logs to facilitate quick diagnosis and resolution.
- User Communication: Clearly inform users about errors, their causes, and potential remedies without exposing sensitive system details.


## Data Flow

1. **Data Ingestion:**
    - Users upload Excel invoices via the Next.js frontend.
    - The backend API receives the uploaded files and stores them securely in **Supabase Storage**.

2. **Data Preprocessing:**
    - The backend processes the raw data using pandas for cleaning and fuzzywuzzy for standardizing column headers.
    - Cleaned data is prepared for AI-driven transformation.

3. **AI Processing:**
    - Preprocessed data is sent to OpenAI’s GPT-4 for intelligent transformation.
    - The AI model interprets and maps data according to predefined prompts tailored to export specifications.

4. **Data Transformation:**
    - Transformed data is further processed to ensure consistency and adherence to the `.xls` format.
    - Finalized data is written into a new `.xls` file using appropriate Python libraries.

5. **Data Storage & Retrieval:**
    - The standardized `.xls` file is stored securely in **Supabase Storage**.
    - A download link is generated and provided to the user for file retrieval via the web interface.

6. **Monitoring & Logging:**
    - All processing activities are logged and monitored via **AWS CloudWatch** and Supabase’s built-in logging features, ensuring transparency and facilitating quick issue resolution.
