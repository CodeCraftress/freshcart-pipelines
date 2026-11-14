# FreshCart Pipelines

**Data Engineering Assignment: From Git to Gold**

Repository: https://github.com/CodeCraftress/freshcart-pipelines

This project demonstrates version control, CI/CD, ELT using Snowflake,
ML pipeline orchestration using Mage, and event streaming using RabbitMQ.

---

## 1. Project Components

| Component | Technology | Purpose |
|---|---|---|
| Version Control | Git and GitHub | Track code changes and collaborate |
| CI/CD | GitHub Actions and pytest | Automatically test code after pushes |
| ELT Pipeline | Snowflake and SQL | Transform raw FreshCart order data |
| ML Pipeline | Mage and Scikit-learn | Train and evaluate an Iris classifier |
| Event Streaming | RabbitMQ and Python | Route food-order events to drivers |

## 2. Repository Structure

```text
freshcart-pipelines/
├── README.md
├── .gitignore
├── requirements.txt
├── mage-requirements.txt
├── elt/
│   ├── freshcart_elt.ipynb
│   ├── freshcart_elt_commented.ipynb
│   └── freshcart_elt_flowchart.html
├── iris_project/
│   ├── metadata.yaml
│   ├── data_loaders/
│   ├── transformers/
│   └── data_exporters/
├── stream/
│   ├── dispatcher.py
│   └── driver.py
├── tests/
│   └── test_prepare_data.py
└── .github/
    └── workflows/
        └── ci.yml
```

## 3. Git Version Control

Git is a distributed version control system. It records changes to project files
and allows developers to maintain a history of their work.

### 3.1 Git's Four Main Areas

The assignment's Git workflow has four stages:

1. **Working folder:** The files and changes currently being developed.
2. **Staging area:** The changes selected for the next commit using `git add`.
3. **Local Git repository:** The committed project history stored locally.
4. **Remote Git repository:** The shared repository hosted on GitHub.

Workflow:

Working folder → Staging area → Local Git → Remote Git → CI/CD

### 3.2 Git Commands and Their Functions

| Git command | Where the change happens | What exactly happens? |
|---|---|---|
| `git init` | Local Git repository | Initializes a new Git repository in the current folder. |
| `git add train.py` | Staging area | Stages the changes in train.py for the next commit. |
| `git commit -m "msg"` | Local Git repository | Saves the staged changes as a new commit in local Git history. |
| `git remote add origin URL` | Local Git configuration | Connects the local repository to a remote repository named origin. |
| `git push -u origin main` | Remote Git repository | Uploads local commits from main to GitHub and sets the upstream branch. |
| `git pull origin main` | Local working folder and repository | Fetches remote changes and integrates them into the current local branch. |

### 3.3 Can a Teammate See Code After git commit?

No. A commit saves the changes only in the local Git repository.
A teammate cannot see those changes on GitHub immediately.

To make the committed code available on GitHub, the developer must run
`git push`. After the push, teammates with repository access can obtain
the latest changes using `git pull`.

### 3.4 Useful Git Commands Used in This Project

```bash
git status
git add .
git commit -m "Meaningful commit message"
git log --oneline
git remote -v
git pull origin main
git push origin main
```

- `git status`: Displays modified, staged and untracked files.
- `git add .`: Stages changes in the current repository.
- `git commit`: Saves staged changes in local history.
- `git log --oneline`: Displays a compact commit history.
- `git remote -v`: Displays configured remote repository URLs.
- `git pull`: Integrates changes from the remote repository.
- `git push`: Publishes local commits to the remote repository.

## 4. Continuous Integration (CI/CD)

### 4.1 What is CI/CD?

Continuous Integration (CI) is the practice of automatically checking and
testing code whenever developers push changes to a shared repository.

Continuous Delivery/Deployment (CD) extends this process by preparing or
releasing validated code for deployment.

In this project, GitHub Actions is used to automate the CI process.

### 4.2 CI Workflow

The workflow is defined in:

`.github/workflows/ci.yml`

It is triggered whenever code is pushed to the main branch or a pull request
targets main.

The workflow performs these steps:

1. **Checkout repository:** Retrieves the source code from GitHub.
2. **Set up Python:** Configures Python 3.12.
3. **Install dependencies:** Installs packages from requirements.txt.
4. **Run tests:** Executes pytest to validate the project code.
5. **Report result:** GitHub Actions displays a successful or failed workflow.

### 4.3 Why is CI Important?

- Detects errors early in the development process.
- Prevents faulty code from being accepted unnoticed.
- Provides repeatable automated testing.
- Improves code reliability and maintainability.
- Gives developers quick feedback after every push.

### 4.4 Pytest and the prepare_data Block

The test file is:

`tests/test_prepare_data.py`

It tests the Iris dataset preparation function from:

`iris_project/transformers/prepare_data.py`

The test checks:

- The expected output keys.
- An 80:20 training and testing split.
- 120 training samples and 30 testing samples.
- Four input features.
- Presence of all three Iris classes in the training set.

Run the test locally:

```bash
python -m pytest -v
```

### 4.5 Successful and Failed CI Runs

Two types of CI execution were demonstrated:

**Successful run:** The test assertions pass and GitHub Actions reports a
green check mark.

**Failed run:** A temporary incorrect expected training sample count was
introduced. Pytest detected the assertion failure and GitHub Actions
reported a red cross.

The original test was subsequently restored and pushed. The final workflow
completed successfully.

This demonstrates how CI detects a problem and verifies its correction.

## 5. Technologies Used

- Python
- Git and GitHub
- GitHub Actions
- pytest
- Pandas and NumPy
- Scikit-learn
- Mage AI
- Snowflake
- SQL
- RabbitMQ
- Pika

## 6. Running Tests

Install the core dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
python -m pytest -v
```

## 7. Project Learning Outcomes

Through this project, the following concepts are demonstrated:

1. Git version control and remote repository management.
2. Automated testing and CI workflow configuration.
3. Data ingestion, transformation and quality validation.
4. ML pipeline orchestration and model evaluation.
5. Topic-based event routing and message acknowledgement.

---

**Project:** From Git to Gold  
**Repository:** https://github.com/CodeCraftress/freshcart-pipelines
