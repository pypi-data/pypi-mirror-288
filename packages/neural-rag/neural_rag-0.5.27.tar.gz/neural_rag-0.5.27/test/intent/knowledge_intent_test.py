import unittest
import os
from pathlib import Path
import shutil
from datetime import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ds_core.properties.property_manager import PropertyManager
from nn_rag.components.commons import Commons
from nn_rag import Knowledge
from nn_rag.intent.knowledge_intent import KnowledgeIntent


# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class KnowledgeIntentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # clean out any old environments
        for key in os.environ.keys():
            if key.startswith('HADRON'):
                del os.environ[key]
        # Local Domain Contract
        os.environ['HADRON_PM_PATH'] = os.path.join('working', 'contracts')
        os.environ['HADRON_PM_TYPE'] = 'parquet'
        # Local Connectivity
        os.environ['HADRON_DEFAULT_PATH'] = Path('working/data').as_posix()
        # Specialist Component
        try:
            os.makedirs(os.environ['HADRON_PM_PATH'])
        except OSError:
            pass
        try:
            os.makedirs(os.environ['HADRON_DEFAULT_PATH'])
        except OSError:
            pass
        try:
            shutil.copytree('../_test_data', os.path.join(os.environ['PWD'], 'working/source'))
        except OSError:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('working')
        except OSError:
            pass

    def test_replace_on_pattern(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        text = "First line.\nSecond line.\r\nThird line.\rFourth line.\n\nParagraph break."
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.replace_on_pattern(tbl)
        print(kn.table_report(result).to_string())

    def test_filter_on_condition(self):
        kn = Knowledge.from_env('tester', has_contract=False)
        tools: KnowledgeIntent = kn.tools
        text = 'You. Me. This is a sentence. An. Another one here. And some more to try.'
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result =  tools.text_to_sentences(tbl, include_score=True)
        print(kn.table_report(result).to_string())
        result = tools.filter_on_condition(result, header='char_count', condition=(5, 'less', None))
        print(kn.table_report(result).to_string())

    def test_filter_on_join_indicies(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        text = ('You took too long. You are not easy to deal with.\n\nPayment Failure/Incorrect Payment.\n\nYou provided '
                'me with incorrect information. Unhappy with delay.\n\nUnsuitable advice. You never answered my question.\n\n'
                'You did not understand my needs.\n\nI have been mis-sold. My details are not accurate.')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_to_paragraphs(tbl)
        print(kn.table_report(result).to_string())
        result = tools.filter_on_join(result, indices=[2, 4])
        print(kn.table_report(result).to_string())

    def test_filter_on_join_chunks(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        text = ('You took too long. You are not easy to deal with. Payment Failure/Incorrect Payment. You provided '
                'me with incorrect information. Unhappy with delay. Unsuitable advice. You never answered my question. '
                'You did not understand my needs. I have been mis-sold. My details are not accurate. You have asked '
                'for too much information. You were not helpful. Payment not generated/received by customer. You did '
                'not keep me updated. Incorrect information given. The performance of my product was poor. No reply '
                'to customer contact. Requested documentation not issued. You did not explain the terms & conditions. '
                'Policy amendments not carried out. You did not explain the next steps/process to me. I cannot '
                'understand your letter/comms. Standard letter inappropriate. Customer payment processed incorrectly. '
                'All points not addressed. Could not understand the agent. Issue with terms and conditions. Misleading '
                'information. I can not use the customer portal. your customer portal is unhelpful')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_to_sentences(tbl)
        result = tools.filter_on_join(result, chunk_size=100)
        print(pc.max(result['text']))
        print(kn.table_report(result).to_string())

    def test_filter_on_mask_index(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        text = ('You took too long. You are not easy to deal with. Payment Failure/Incorrect Payment.\n\nYou provided '
                'me with incorrect information. Unhappy with delay.\n\nUnsuitable advice. You never answered my question.'
                'You did not understand my needs.\n\nI have been mis-sold. My details are not accurate.')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_to_paragraphs(tbl)
        print(kn.table_report(result, head=5).to_string())
        result = tools.filter_on_mask(result, indices=[0, (2, 7)])
        print(kn.table_report(result, head=5).to_string())

    def test_filter_on_mask_pattern(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        text = ('You took too long. You are not easy to deal with. Payment Failure/Incorrect Payment.\n\nYou provided '
                'me with incorrect information. Unhappy with delay.\n\nUnsuitable advice. You never answered my question.'
                'You did not understand my needs.\n\nI have been mis-sold. My details are not accurate.')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_to_paragraphs(tbl)
        print(kn.table_report(result, head=5).to_string())
        result = tools.filter_on_mask(result, pattern='^You.*(You|Unhappy)')
        print(kn.table_report(result).to_string())

    def test_text_from_markdown(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        text = """
# Markdown Cheat Sheet
This Markdown cheat sheet provides a quick overview of all the Markdown syntax elements. 

## Basic Syntax
These are the elements outlined in John Gruber’s original design document.

### Heading
# H1
## H2
### H3

**bold text**

*italicized text*
               
### Ordered List
1. First item
2. Second item
3. Third item
        """
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_from_markdown(tbl)
        print(kn.table_report(result, head=6).to_string())

    def test_text_to_paragraph(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        # uri = "https://assets.circle.so/kvx4ix1f5ctctk55daheobna46hf"
        # tbl = kn.set_source_uri(uri).load_source_canonical()
        text = ('You took too long. You are not easy to deal with. Payment Failure/Incorrect Payment. You provided '
                'me with incorrect information. Unhappy with delay. Unsuitable advice. You never answered my question.\n\n'
                'You took too long. You are not easy to deal with. Payment Failure/Incorrect Payment. You provided '
                'me with incorrect information. Unhappy with delay. Unsuitable advice. You never answered my question.\n\n'
                'You did not understand my needs. I have been mis-sold. My details are not accurate. You have asked '
                'for too much information. You were not helpful. Payment not generated/received by customer. You did '
                'not keep me updated. Incorrect information given. The performance of my product was poor.\n\n No reply '
                'to customer contact. Requested documentation not issued. You did not explain the terms & conditions.\n\n'
                'Policy amendments not carried out. You did not explain the next steps/process to me. I cannot '
                'understand your letter/comms. Standard letter inappropriate. Customer payment processed incorrectly.\n\n'
                'All points not addressed. Could not understand the agent. Issue with terms and conditions. Misleading '
                'information. I can not use the customer portal. your customer portal is unhelpful.')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_to_paragraphs(tbl, include_score=True)
        print(kn.table_report(result, head=6).to_string())

    def test_text_to_paragraph_regex(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        text = ('Badguys AI Ethics and Responsible AI Policy At Badguys, This policy outlines our '
                'commitment to ethical AI practices:\n1. Ethical Principles:\na. Transparency: We '
                'commit to transparency in our AI systems design,\nb. Fairness and Equity: We will '
                'ensure that our AI technologies do not propagate bias\n2. Data Governance:\na. Data '
                'Quality:\nb. User Consent:\n3. AI Development and Deployment: a. Continuous '
                'Evaluation:\nb. Human Oversight: ')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        # result = tools.text_to_paragraphs(tbl, pattern='\n')
        result = tools.text_to_paragraphs(tbl, pattern=r"\d+\.\s[A-Z]")
        # result = tools.text_to_paragraphs(tbl)
        print(kn.table_report(result).to_string())

    def test_text_to_document(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        text = ('You took too long. You are not easy to deal with. Payment Failure/Incorrect Payment.\n\nYou provided '
                'me with incorrect information. Unhappy with delay.\n\nUnsuitable advice. You never answered my question.'
                'You did not understand my needs.\n\nI have been mis-sold. My details are not accurate.')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_to_paragraphs(tbl, include_score=False)
        print(kn.table_report(result, head=5).to_string())
        result = tools.text_to_document(result)
        print(kn.table_report(result, head=5).to_string())

    def test_text_to_sentence(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        text = ('You took too long and you are not easy to deal with regarding Payment Failure/Incorrect Payment. '
                'You took too long and you are not easy to deal with regarding Payment Failure/Incorrect Payment. '
                'You provided me with incorrect information. Unhappy with delay. Unsuitable advice. You never answered my question. '
                'You did not understand my needs. You did not understand my needs. I have been mis-sold.')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_to_sentences(tbl, include_score=True)
        print(kn.table_report(result).to_string())

    def test_text_to_sentence_max(self):
        kn = Knowledge.from_env('tester', has_contract=False)
        tools: KnowledgeIntent = kn.tools
        text = ('You took too long. You are not easy to deal with. Payment Failure/Incorrect Payment. You provided '
                'me with incorrect information. Unhappy with delay. Unsuitable advice. You never answered my question. '
                'You did not understand my needs. I have been mis-sold. My details are not accurate. You have asked '
                'for too much information. You were not helpful. Payment not generated/received by customer. You did '
                'not keep me updated. Incorrect information given. The performance of my product was poor. No reply '
                'to customer contact. Requested documentation not issued. You did not explain the terms & conditions. '
                'Policy amendments not carried out. You did not explain the next steps/process to me. I cannot '
                'understand your letter/comms. Standard letter inappropriate. Customer payment processed incorrectly. '
                'All points not addressed. Could not understand the agent. Issue with terms and conditions. Misleading '
                'information. I can not use the customer portal. your customer portal is unhelpful')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        # uri = "https://pressbooks.oer.hawaii.edu/humannutrition2/open/download?type=pdf"
        # tbl = kn.set_source_uri(uri, file_type='pdf').load_source_canonical()
        result =  tools.text_to_sentences(tbl, char_limit=10)
        print(kn.table_report(result, head=5).to_string())

    def test_text_to_sentence_score(self):
        kn = Knowledge.from_env('tester', has_contract=False)
        tools: KnowledgeIntent = kn.tools
        text = ('You took too long. You took too long. You were slow. You are not easy to deal with.'
                'You were hard work. I did not get what I asked for. The product was wrong.')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        # uri = "https://pressbooks.oer.hawaii.edu/humannutrition2/open/download?type=pdf"
        # tbl = kn.set_source_uri(uri, file_type='pdf').load_source_canonical()
        result =  tools.text_to_sentences(tbl, include_score=True)
        print(kn.table_report(result).to_string())

    def test_text_to_chunks(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        # uri = "https://assets.circle.so/kvx4ix1f5ctctk55daheobna46hf"
        # kn.set_source_uri(uri)
        # tbl = kn.load_source_canonical(file_type='pdf')
        text = ('You took too long. You took too long. You are not easy to deal with. Payment Failure/Incorrect Payment. You provided '
                'me with incorrect information. Unhappy with delay. Unsuitable advice. You never answered my question. '
                'You did not understand my needs. I have been mis-sold. My details are not accurate. You have asked '
                'for too much information. You were not helpful. Payment not generated/received by customer. You did '
                'not keep me updated. Incorrect information given. The performance of my product was poor. No reply '
                'to customer contact. Requested documentation not issued. You did not explain the terms & conditions. '
                'Policy amendments not carried out. You did not explain the next steps/process to me. I cannot '
                'understand your letter/comms. Standard letter inappropriate. Customer payment processed incorrectly. '
                'All points not addressed. Could not understand the agent. Issue with terms and conditions. Misleading '
                'information. I can not use the customer portal. your customer portal is unhelpful')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_to_chunks(tbl)
        print(kn.table_report(result).to_string())

    def test_text_chunk_semantic(self):
        kn = Knowledge.from_memory()
        tools: KnowledgeIntent = kn.tools
        # uri = "https://www.europarl.europa.eu/doceo/document/TA-9-2024-0138_EN.pdf"
        # kn.set_source_uri(uri)
        # tbl = kn.load_source_canonical(file_type='pdf')
        text = ('You took too long. You took too long. You are not easy to deal with. Payment Failure/Incorrect Payment. You provided '
                'me with incorrect information. Unhappy with delay. Unhappy with delay. Unsuitable advice. You never answered my question. '
                'You did not understand my needs. I have been mis-sold. My details are not accurate. You have asked '
                'for too much information. You were not helpful. Payment not generated/received by customer. You did '
                'not keep me updated. Incorrect information given. The performance of my product was poor. No reply '
                'to customer contact. Requested documentation not issued. You did not explain the terms & conditions. '
                'Policy amendments not carried out. You did not explain the next steps/process to me. I cannot '
                'understand your letter/comms. Standard letter inappropriate. Customer payment processed incorrectly. '
                'All points not addressed. Could not understand the agent. Issue with terms and conditions. Misleading '
                'information. I can not use the customer portal. your customer portal is unhelpful')
        arr = pa.array([text], pa.string())
        tbl = pa.table([arr], names=['text'])
        result = tools.text_to_chunks(tbl, chunk_size=100)
        print(kn.table_report(result).to_string())

    # def test_text_from_load(self):
    #     kn = Knowledge.from_memory()
    #     tools: KnowledgeIntent = kn.tools
    #     uri = '../../jupyter/knowledge/hadron/source/Global-Index-1st-Edition-Report.pdf'
    #     kn.set_source_uri(uri)
    #     tbl = kn.load_source_canonical(file_type='pdf', as_pages=True, as_markdown=True)
    #     result = tbl.filter(pc.greater(tbl['table_count'], 0))
    #     print(result.shape)

    def test_raise(self):
        startTime = datetime.now()
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))
        print(f"Duration - {str(datetime.now() - startTime)}")

def get_table():
    n_legs = pa.array([2, 4, 5, 100])
    animals = pa.array(["Flamingo", "Horse", "Brittle stars", "Centipede"])
    names = ["n_legs", "animals"]
    return pa.Table.from_arrays([n_legs, animals], names=names)


def tprint(t: pa.table, top: int=None, headers: [str, list]=None, d_type: [str, list]=None, regex: [str, list]=None):
    top = top if isinstance(top, int) else 10
    _ = Commons.filter_columns(t.slice(0, top), headers=headers, d_types=d_type, regex=regex)
    print(Commons.table_report(_).to_string())


if __name__ == '__main__':
    unittest.main()
