from django.test import TestCase
from workflow.models import Company, Job
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
