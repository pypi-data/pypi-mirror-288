import unittest
import pandas as pd
from text_preprocess_sanitizer.preprocess import text_sanitizer

class TestStrProcessing(unittest.TestCase):
    def setUp(self):
        # Sample data simulating ITSM ticket content
        self.data = pd.Series([
        # English
        "Amit Kumar Gaurav Singh ITSM Ticket ID: TKT-0001 - User: John Doe reported a system outage at 1234-5678-9123-4567. Issue: Network connectivity problems across multiple sites, Sumit didn't do his job well. Resolution: Router rebooted, connectivity restored, Vichitra diagnosed. Vinod manufacturers are corrupt. 2024-08-03 09:15:00 Please connect me at : pax@proton.me",
        "Ticket: TKT-0002 - Jane Smith reported her phone 987-654-3210 being unresponsive. Analysis: Hardware failure suspected. Action: Replacement phone dispatched. Contact: (202) 555-0184, visit www.example.com for more info.",
        
        # German
        "Hans Müller, 1234-5678-9123-4567, die Daten sind für die Erstellung eines Tickets geeignet gauravds@gmail.com www.google.com",
        "Serviceanfrage: SR-2024-0005 - Eingereicht von: Hans Müller. Anfrage für Software-Update auf allen Systemen. Geplant für: 2024-08-05. Status: Abgeschlossen. Kontakt: 1234-5678-9123-4567 zur Bestätigung.",
        
        # French
        "Incident ID: 2024-0003 - Reported by: Jean Dupont. Issue: Unable to access corporate VPN. Troubleshooting steps: Checked firewall settings, no issues found. Resolution pending. Contact: 1234-5678-9123-4567",
        "ITSM Case: 2024-0004 - Marie Curie faced login issues with email. Error: 'Invalid credentials'. Reset password and advised user to try again. Support contact: 987-654-3210. Further details at www.exemple.fr.",
        
        # Italian
        "Incident Report: IR-2024-0008 - Luca Bianchi encountered a security breach attempt. Mitigation: Enhanced firewall rules applied. Ongoing monitoring by security team. Report issues to 987-654-3210 or visit www.esempio.it",
        "Problem Ticket: PRB-2024-0007 - Giovanni Rossi reported persistent database errors. Cause: Corrupted tables. Action: Data restoration underway. Contact support at 1234-5678-9123-4567.",
        
        # Spanish
        "Informe de incidente: IR-2024-0009 - Luis Gómez informó un error al acceder al sistema. Acción: Reinicio del sistema, monitoreo continuo. Contacto: 987-654-3210 o visite www.ejemplo.es para más información.",
        "Solicitud de servicio: SR-2024-0010 - Solicitado por: Carmen Rodríguez. Solicitud de actualización de software en todos los servidores. Programado para: 2024-08-06. Estado: En progreso. Contacto: 1234-5678-9123-4567 para confirmación.",
        
        # Portuguese
        "Relatório de Incidente: RI-2024-0009 - Maria Silva encontrou um erro no sistema ao acessar o portal. Ação: Reinício do sistema, monitoramento contínuo. Contato: 987-654-3210 ou acesse www.exemplo.com.br para mais informações.",
        "Pedido de Serviço: PS-2024-0010 - Solicitado por: João Souza. Solicitação de atualização de software em todos os servidores. Programado para: 2024-08-06. Status: Em andamento. Contate: 1234-5678-9123-4567 para confirmação.",
        
        # Dutch
        "Incidentrapport: IR-2024-0012 - Jan de Vries merkte een poging tot beveiligingsinbraak op. Maatregel: Verhoogde firewallregels toegepast. Lopende monitoring door het beveiligingsteam. Meld problemen op 987-654-3210 of bezoek www.voorbeeld.nl",
        "Serviceverzoek: SV-2024-0013 - Ingediend door: Emma Janssen. Verzoek om software-update op alle systemen. Gepland voor: 2024-08-07. Status: Voltooid. Neem contact op: 1234-5678-9123-4567 voor bevestiging."
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
            # English
            self.assertNotIn('John Doe', text, "Name 'John Doe' was not removed as expected.")
            self.assertNotIn('Jane Smith', text, "Name 'Jane Smith' was not removed as expected.")
            
            # German
            self.assertNotIn('Hans Müller', text, "Name 'Hans Müller' was not removed as expected.")
            
            # French
            self.assertNotIn('Jean Dupont', text, "Name 'Jean Dupont' was not removed as expected.")
            self.assertNotIn('Marie Curie', text, "Name 'Marie Curie' was not removed as expected.")
            
            # Italian
            self.assertNotIn('Giovanni Rossi', text, "Name 'Giovanni Rossi' was not removed as expected.")
            self.assertNotIn('Luca Bianchi', text, "Name 'Luca Bianchi' was not removed as expected.")
            
            # Spanish
            self.assertNotIn('Luis Gómez', text, "Name 'Luis Gómez' was not removed as expected.")
            self.assertNotIn('Carmen Rodríguez', text, "Name 'Carmen Rodríguez' was not removed as expected.")
            
            # Portuguese
            self.assertNotIn('Maria Silva', text, "Name 'Maria Silva' was not removed as expected.")
            self.assertNotIn('João Souza', text, "Name 'João Souza' was not removed as expected.")
            
            # Dutch
            self.assertNotIn('Jan de Vries', text, "Name 'Jan de Vries' was not removed as expected.")
            self.assertNotIn('Emma Janssen', text, "Name 'Emma Janssen' was not removed as expected.")
            
            # Phone Numbers
            self.assertNotIn('987-654-3210', text, "Phone number '987-654-3210' was not removed as expected.")
            self.assertNotIn('1234-5678-9123-4567', text, "Phone number '1234-5678-9123-4567' was not removed as expected.")
            self.assertNotIn('(202) 555-0184', text, "Phone number '(202) 555-0184' was not removed as expected.")

        print("✅ Sensitive information has been expertly sanitized. Data processed successfully and ready for further use")
        

if __name__ == '__main__':
    unittest.main()
