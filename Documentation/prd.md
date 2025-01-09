# Product Requirements Document (PRD)

## Project Overview

### Objective
Automate the processing of client invoices to eliminate manual formatting and reduce errors, ensuring all processed invoices meet the export department’s standardized `.xls` format requirements.

### Input
- **Format:** Excel invoice files provided by various clients.
- **Variability:**
  - Different column orders.
  - Presence of additional, irrelevant columns.
  - Slight variations in column header names (e.g., "Product Code" vs. "Style Code").

### Output
- **Format:** Excel files (`.xls`) formatted according to the export department’s specifications.
- **Requirements:**
  - Include all essential fields as outlined by the export department.
  - Ensure consistent data types and standardized formats (values, not formulas).

## Technical Approach

### Chosen Strategy
**AI-Based Automated Transformation**

#### Reasoning
- Handles varying column orders and additional irrelevant columns without the need for individual templates per client.
- Scalable solution adaptable to new clients.
- Aligns with stakeholder preference for AI-driven solutions, enhancing project visibility and support.

### Technology Stack
- **Cloud Hosting & Backend Services:** Supabase
  - **Database:** PostgreSQL managed by Supabase for storing user data, invoice metadata, and processed file references.
  - **Authentication:** Supabase Auth for managing user authentication and authorization.
  - **Storage:** Supabase Storage for storing uploaded and processed invoice files securely.
- **Machine Learning:** OpenAI GPT-3.5 Turbo or GPT-4
- **Web Application:** Next.js (Frontend) and FastAPI (Backend)
- **Deployment:** AWS EC2
- **Security:** HTTPS for secure data transmission and Supabase’s built-in security features.
- **Data Processing:** Python with pandas and fuzzywuzzy libraries.

## Project Phases and Roadmap

1. **Planning and Requirements Finalization**
   - **Activities:**
     - Finalize the list of required fields and output formats with the export department.
     - Define success metrics and performance benchmarks.
   - **Reasoning:** Establishing clear requirements ensures that the solution meets all stakeholder needs and sets measurable goals for the project.

2. **Infrastructure Setup**
   - **Activities:**
     - Set up AWS environment, including IAM roles and permissions.
     - Configure necessary AWS services for hosting the web application (e.g., EC2, S3).
     - Implement secure data transmission (HTTPS) by obtaining and installing SSL certificates.
   - **Reasoning:** A robust and secure infrastructure is foundational for deploying the application reliably.

3. **Data Preparation**
   - **Activities:**
     - **Data Collection:** Gather sample invoices from all clients to understand the variability and structure.
     - **Data Organization:** Store collected invoices in a structured directory, categorized by client and date.
   - **Reasoning:** Even when using pre-trained models, having a representative dataset is crucial for testing and validating the system’s performance with real-world data variations.

4. **Integration with OpenAI API**
   - **Activities:**
     - Set up API access and manage OpenAI API keys securely.
     - Develop integration layers to interact with OpenAI’s models for data transformation tasks.
     - Implement prompt engineering to tailor the AI’s responses to your specific invoice processing needs.
   - **Reasoning:** Effective integration ensures that the AI can accurately interpret and transform invoice data according to the required specifications.

5. **Web Interface Development**
   - **Activities:**
     - Build the file upload interface using Next.js, including form validation and user feedback.
     - Implement backend processing logic in FastAPI to handle uploaded files, interact with the OpenAI API, and process responses.
     - Create the download interface for users to retrieve processed `.xls` files.
   - **Reasoning:** A user-friendly interface is essential for seamless interactions between the export department users and the automated processing system.

6. **Data Transformation Logic**
   - **Activities:**
     - Utilize pandas for data manipulation and cleaning.
     - Apply fuzzywuzzy for fuzzy string matching to handle variations in column headers.
     - Develop scripts to map and transform data into the standardized `.xls` format.
   - **Reasoning:** Ensuring data consistency and correctness is critical for the reliability of the output files.

7. **Testing**
   - **Activities:**
     - **Unit Testing:** Test individual components such as file upload, data processing, and file download functionalities.
     - **Integration Testing:** Ensure that all components work together seamlessly.
     - **User Acceptance Testing (UAT):** Conduct UAT with export department users to gather feedback and make necessary adjustments.
   - **Reasoning:** Comprehensive testing guarantees that the system functions as intended and meets user expectations.

8. **Deployment**
   - **Activities:**
     - Deploy the web application to the AWS production environment.
     - Set up monitoring and logging using AWS CloudWatch.
     - Implement backup and recovery procedures to ensure data integrity and availability.
   - **Reasoning:** A smooth deployment process ensures that the application is accessible and reliable for end-users.

9. **User Training and Documentation**
   - **Activities:**
     - Create comprehensive user guides and documentation for the export department.
     - Conduct training sessions or webinars to onboard users.
   - **Reasoning:** Proper training and documentation empower users to effectively utilize the new system, maximizing its benefits.

10. **Maintenance and Continuous Improvement**
    - **Activities:**
      - Monitor system performance and address any issues promptly.
      - Collect user feedback to identify areas for enhancement.
      - Plan for periodic reviews and updates to incorporate new features or improvements based on user needs and technological advancements.
    - **Reasoning:** Ongoing maintenance ensures the system remains reliable and evolves to meet changing requirements.

## Project Constraints and Considerations

- **Budget:** Limited budget; solution must be cost-effective.
- **User Base:** Approximately 10 users in the export department.
- **Performance:** Aim for high accuracy (98%+) and quick processing times.

## Key Tools and Libraries

- **Programming Language:** Python
- **Web Framework:** React and FastAPI
- **Data Processing:** pandas, fuzzywuzzy
- **Machine Learning:** OpenAI
- **Deployment:** AWS Elastic Beanstalk or AWS EC2
- **Security:** HTTPS, IAM roles