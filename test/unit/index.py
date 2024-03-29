import unittest
import coverage
from ModificaOrdineTest import ModificaOrdineTest
from EliminaAccountTest import EliminaAccountTest
from LoginTest import LoginTest
from ModificaProdottoTest import ModificaProdottoTest
from ModificaPersonaleTest import ModificaPersonaleTest
from RegisterTest import RegisterTest
from SearchProductTest import SearchProductTest
from AggiungiDatiSpedizioneTest import AggiungiDatiSpedizioneTest
from AggiungiProdottoTest import AggiungiProdottoTest
from RicercaNLPTest import RicercaNLPTest


if __name__ == '__main__':
    cov = coverage.Coverage(branch=True)
    cov.start()

    loader = unittest.TestLoader()
    modifica_ordine_suite = loader.loadTestsFromTestCase(ModificaOrdineTest)
    elimina_account_suite = loader.loadTestsFromTestCase(EliminaAccountTest)
    login_suite = loader.loadTestsFromTestCase(LoginTest)
    modifica_prodotto_suite = loader.loadTestsFromTestCase(ModificaProdottoTest)
    modifica_personale_suite = loader.loadTestsFromTestCase(ModificaPersonaleTest)
    register_suite = loader.loadTestsFromTestCase(RegisterTest)
    search_product_suite = loader.loadTestsFromTestCase(SearchProductTest)
    aggiungi_indirizzo_suite = loader.loadTestsFromTestCase(AggiungiDatiSpedizioneTest)
    aggiungi_prodotto_suite = loader.loadTestsFromTestCase(AggiungiProdottoTest)
    ricerca_nlp_suite = loader.loadTestsFromTestCase(RicercaNLPTest)

    all_tests = unittest.TestSuite([modifica_ordine_suite, elimina_account_suite, login_suite, modifica_prodotto_suite,
                                    modifica_personale_suite, register_suite, search_product_suite,
                                    aggiungi_indirizzo_suite, aggiungi_prodotto_suite, ricerca_nlp_suite])

    unittest.TextTestRunner(verbosity=2).run(all_tests)

    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory='coverage_html_report')
