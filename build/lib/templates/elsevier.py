# -*- coding: utf-8 -*-
from .methods import Methods
import re

class ElsevierTemplate(Methods):
    '''Template for PDFs from Elsevier'''

    def __init__(self, pdf):
        '''
        :param pdf: PDF extracted in ordered textblocks with features added
        :param extraction_pattern: Unique regex pattern for section title extraction of Elsevier
        :param metadata: Metadata extracted by default get_metadata() method, containing abstract, keywords, doi, figure caption and title
        '''
        Methods.__init__(self)
        self.pdf = pdf
        self.extraction_pattern = '^[A-Z][a-z]+$|\d\.\s[A-Z]*[a-z]*(\s)*.+("\n")*.+|^\d\.\s[A-Z]*[a-z]+(\s[A-Z]*[a-z]*)+|^(?i)Reference(s)*(\s)*.+|^Acknowledg(e)*ment(s)*'
        self.metadata = self.get_metadata(pdf)

    def test(self):
        '''Check if template is returned by extraction function'''
        print('PDF returned successfully')

    def author(self):
        '''Temporarily taken down'''
        pass

    def reference(self):
        '''Seperate reference part from the whole PDF'''
        return self.get_reference(self.section())

    def section(self):
        '''Extract section title and corresponding text'''
        return self.get_section(self.pdf, self.extraction_pattern, pub = 'els')

    def plaintext(self):
        return self.get_puretext(self.pdf)

    def journal(self, info_type=None):
        '''
        Extract journal information, info_type including jounal name, year, volume and page

        :param info_type: user-defined argument used to select jounal name, year, volume or page
        '''
        journal = {'name':'',
                   'year':'',
                   'volume':'',
                   'page':''
                   }

        for key, value in self.pdf.items():
            '''
            Elsevier has its journal placed at the top the first page, 
            thus information can be extracted for this textblock.
            '''
            if key[0] == 0:#check if current page is the first page
                if value['universal_sequence'] == 1:#check if current textblock is the first one on this page
                    text = re.findall('\d+', value['text'])
                    if text:
                        journal['name'] = value['text']
                        journal['volume'] = text[0]
                        journal['year'] = text[1]
                        journal['page'] = '-'.join(text[2:])

        if info_type == None:
            return journal
        else:
            return journal[info_type]

    def doi(self):
        return self.metadata['doi']

    def title(self):
        return self.metadata['title']

    def keywords(self):
        return self.metadata['keywords']

    def abstract(self):
        return self.metadata['abstract']

    def caption(self, nicely=False):
        if nicely == True:
            for seq, caption in self.metadata['figure'].items():
                print(seq)
                print(caption)
                print('\n')
        return self.metadata['figure']