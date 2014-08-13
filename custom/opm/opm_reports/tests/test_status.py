from datetime import date
from custom.opm.opm_reports.constants import InvalidRow
from custom.opm.opm_reports.tests import OPMCaseReportTestBase, OPMCase, MockCaseRow


class TestPregnancyStatus(OPMCaseReportTestBase):

    def test_not_yet_delivered(self):
        case = OPMCase(
            forms=[],
            edd=date(2014, 12, 10),
        )
        row = MockCaseRow(case, self.report)
        self.assertEqual('pregnant', row.status)

    def test_delivered_before_period(self):
        case = OPMCase(
            forms=[],
            edd=date(2014, 3, 10),
            dod=date(2014, 3, 10),
        )
        row = MockCaseRow(case, self.report)
        self.assertEqual('mother', row.status)

    def test_delivered_after_period(self):
        case = OPMCase(
            forms=[],
            edd=date(2014, 9, 10),
            dod=date(2014, 9, 10),
        )
        row = MockCaseRow(case, self.report)
        self.assertEqual('pregnant', row.status)

    def test_no_valid_status(self):
        case = OPMCase(
            forms=[],
        )
        self.assertRaises(InvalidRow, MockCaseRow, case, self.report)

    def test_due_before_period_not_delivered(self):
        case = OPMCase(
            forms=[],
            edd=date(2014, 3, 10),
        )
        self.assertRaises(InvalidRow, MockCaseRow, case, self.report)

    def test_due_in_period_not_delivered(self):
        case = OPMCase(
            forms=[],
            edd=date(2014, 6, 10),
        )
        # todo: is this really right? this person won't count to either status in the month
        # is that valid given that people deliver late? (maybe yes since they have already had 6 months counting
        self.assertRaises(InvalidRow, MockCaseRow, case, self.report)
