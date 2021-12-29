from django.test import TestCase
from workflow.models import Application, Company, Job, User
import datetime


class CompanyTest(TestCase):
    def setUp(self) -> None:
        self.company = Company(
            name='Some company',
            created_at=datetime.datetime.now()
        )

    def test_model_can_create_a_company(self) -> None:
        old_count = Company.objects.count()
        self.company.save()
        new_count = Company.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_it_has_jobs(self) -> None:
        self.company.save()

        Job.objects.create(
            company_id=self.company.id,
            title='A job',
            category='Engineering',
            created_at=datetime.datetime.now()
        )

        self.assertEqual(1, self.company.jobs.count())


class JobTest(TestCase):
    def setUp(self) -> None:
        self.company = Company(
            name='Some company',
            created_at=datetime.datetime.now()
        )
        self.company.save()

        self.job = Job(
            company_id=self.company.id,
            title='A job',
            category='Engineering',
            created_at=datetime.datetime.now()
        )

    def test_model_can_create_a_job(self) -> None:
        old_count = Job.objects.count()
        self.job.save()
        new_count = Job.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_it_belongs_to_a_company(self) -> None:
        self.job.save()

        self.assertEqual(self.job.company_id, self.company.id)
        self.assertIsInstance(self.job.company, Company)


class ApplicationTest(TestCase):
    def setUp(self) -> None:
        self.company = Company(
            name='Some company',
            created_at=datetime.datetime.now()
        )
        self.company.save()

        self.job = Job(
            company_id=self.company.id,
            title='A job',
            category='Engineering',
            created_at=datetime.datetime.now()
        )
        self.job.save()

        self.applicant = User(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            phone='+33123456789',
            email='email@email.com'
        )
        self.applicant.save()

        self.application = Application(
            applicant_id=self.applicant.id,
            job_id=self.job.id,
            created_at=datetime.datetime.now()
        )

    def test_model_can_create_an_application(self) -> None:
        old_count = Application.objects.count()
        self.application.save()
        new_count = Application.objects.count()

        self.assertNotEqual(old_count, new_count)

    def test_it_belongs_to_a_job(self) -> None:
        self.application.save()

        self.assertEqual(self.application.job_id, self.job.id)
        self.assertIsInstance(self.application.job, Job)

    def test_it_belongs_to_an_applicant(self) -> None:
        self.application.save()

        self.assertEqual(self.application.applicant_id, self.applicant.id)
        self.assertIsInstance(self.application.applicant, User)
