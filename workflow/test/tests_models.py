from django.test import TestCase
from authentication.models import User
from workflow.models import Application, Company, Job
from workflow.factories import ApplicationFactory, CompanyFactory, JobFactory, UserFactory


class CompanyTest(TestCase):
    def test_a_company_can_be_created(self) -> None:
        old_count = Company.objects.count()
        CompanyFactory()
        new_count = Company.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_a_company_has_jobs(self) -> None:
        company = CompanyFactory()

        self.assertEqual(1, company.jobs.count())


class JobTest(TestCase):
    def test_a_job_can_be_created(self) -> None:
        old_count = Job.objects.count()
        JobFactory()
        new_count = Job.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_a_job_belongs_to_a_company(self) -> None:
        company = CompanyFactory()
        job = JobFactory(company_id=company.id)

        self.assertEqual(job.company_id, company.id)
        self.assertIsInstance(job.company, Company)


class ApplicationTest(TestCase):
    def test_an_application_can_be_created(self) -> None:
        old_count = Application.objects.count()
        ApplicationFactory()
        new_count = Application.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_an_application_belongs_to_a_job(self) -> None:
        job = JobFactory()
        application = ApplicationFactory(job_id=job.id)

        self.assertEqual(application.job_id, job.id)
        self.assertIsInstance(application.job, Job)

    def test_an_application_belongs_to_an_applicant(self) -> None:
        applicant = UserFactory()
        application = ApplicationFactory(applicant_id=applicant.id)

        self.assertEqual(application.applicant_id, applicant.id)
        self.assertIsInstance(application.applicant, User)
