import unittest
import pandas as pd
from text_preprocess_sanitizer.preprocess import text_sanitizer

class TestStrProcessing(unittest.TestCase):
    def setUp(self):
        # Sample data simulating ITSM ticket content
        self.data = pd.Series([
            "Amit Kumar Gaurav Singh ITSM Ticket ID: TKT-0001 - User: John Doe reported a system outage at 1234-5678-9123-4567. Issue: Network connectivity problems across multiple sites, Sumit didn't do his job well. Resolution: Router rebooted, connectivity restored, Vichitra diagnosed. Vinod manufacturers are corrupt. 2024-08-03 09:15:00 Please connect me at : pax@proton.me",
            "Amit Kumar Gaurav Singh ITSM Ticket ID: TKT-0001 - User: John Doe reported a system outage at 1234-5678-9123-4567. Issue: Network connectivity problems across multiple sites, Sumit didn't do his job well. Resolution: Router rebooted, connectivity restored, Vichitra diagnosed. Vinod manufacturers are corrupt. 2024-08-03 09:15:00. Contact pax@proton.me",
            "Amit Kumar Gaurav Singh ITSM Ticket ID: TKT-0001 - User: John Doe reported a system outage at 1234-5678-9123-4567. Issue: Network connectivity problems across multiple sites, Sumit didn't do his job well. Resolution: Router rebooted, connectivity restored, Vichitra diagnosed. Vinod manufacturers are corrupt. 2024-08-03 09:15:00. Contact us at pax@proton.me",
            "Ticket: TKT-0002 - Jane Smith reported her phone 987-654-3210 being unresponsive. Analysis: Hardware failure suspected. Action: Replacement phone dispatched. Contact: (202) 555-0184, visit www.example.com for more info.",
            "Incident ID: 2024-0003 - Reported by: Jean Dupont. Issue: Unable to access corporate VPN. Troubleshooting steps: Checked firewall settings, no issues found. Resolution pending. Contact: 1234-5678-9123-4567",
            "ITSM Case: 2024-0004 - Marie Curie faced login issues with email. Error: 'Invalid credentials'. Reset password and advised user to try again. Support contact: 987-654-3210. Further details at www.exemple.fr.",
            "Service Request: SR-2024-0005 - Submitted by: Hans Müller. Request for software update on all systems. Scheduled for: 2024-08-05. Status: Completed. Contact: 1234-5678-9123-4567 for confirmation.",
            "Change Request: CR-2024-0006 - Anna Schmidt requested changes to server configurations. Approved by IT admin. Implementation: 2024-08-07. Post-implementation review scheduled. Contact: (202) 555-0184",
            "Problem Ticket: PRB-2024-0007 - Giovanni Rossi reported persistent database errors. Cause: Corrupted tables. Action: Data restoration underway. Contact support at 1234-5678-9123-4567.",
            "Incident Report: IR-2024-0008 - Luca Bianchi encountered a security breach attempt. Mitigation: Enhanced firewall rules applied. Ongoing monitoring by security team. Report issues to 987-654-3210 or visit www.esempio.it",
            "Hans Müller, 1234-5678-9123-4567, die Daten sind für die Erstellung eines Tickets geeignet gauravds@gmail.com www.google.com"
        ])
        
        

    def test_processing(self):
        # Process the data
        processed_data = text_sanitizer(self.data)

        # Print processed data for inspection
        print("\nProcessed Data:")
        for i, text in enumerate(processed_data, start=1):
            print(f"Entry {i}: {text}\n")

        # Assertions to ensure sensitive information is removed
        for text in processed_data:
            self.assertNotIn('John Doe', text, "Name 'John Doe' was not removed as expected.")
            self.assertNotIn('Jane Smith', text, "Name 'Jane Smith' was not removed as expected.")
            self.assertNotIn('987-654-3210', text, "Phone number '987-654-3210' was not removed as expected.")
            self.assertNotIn('Jean Dupont', text, "Name 'Jean Dupont' was not removed as expected.")
            self.assertNotIn('Marie Curie', text, "Name 'Marie Curie' was not removed as expected.")
            self.assertNotIn('Hans Müller', text, "Name 'Hans Müller' was not removed as expected.")
            self.assertNotIn('Anna Schmidt', text, "Name 'Anna Schmidt' was not removed as expected.")
            self.assertNotIn('Giovanni Rossi', text, "Name 'Giovanni Rossi' was not removed as expected.")
            self.assertNotIn('Luca Bianchi', text, "Name 'Luca Bianchi' was not removed as expected.")

        print("✅ Sensitive information has been expertly sanitized. Data processed successfully and ready for further processing.")
        

if __name__ == '__main__':
    unittest.main()
