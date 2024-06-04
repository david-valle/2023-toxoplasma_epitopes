from unittest import TestCase
from web_utilities.HTMLTableStripper import HTMLTableStripper, HTMLParseError

class HTMLTableStripperTests(TestCase):
    def basic_tests(self):
        html_results = '''
            <tr class="odd"><td>HLA-DRB1*01:01</td><td>1</td><td>2</td><td>16</td><td class="sequence">IIGKKDKDGEGAPPA</td><td>Consensus (comb.lib./smm/nn)</td><td>84.52</td><td class="show_hide">KDGEGAPPA</td><td class="show_hide">187971.76</td><td class="show_hide">84.52</td><td class="show_hide">IIGKKDKDG</td><td class="show_hide">7531</td><td class="show_hide">88.48</td><td class="show_hide">KDGEGAPPA</td><td class="show_hide">2595.20</td><td class="show_hide">81.51</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td></tr>
            <tr class="even"><td>HLA-DRB1*01:01</td><td>1</td><td>3</td><td>17</td><td class="sequence">IGKKDKDGEGAPPAK</td><td>Consensus (comb.lib./smm/nn)</td><td>84.52</td><td class="show_hide">KDGEGAPPA</td><td class="show_hide">187971.76</td><td class="show_hide">84.52</td><td class="show_hide">KDGEGAPPA</td><td class="show_hide">9417</td><td class="show_hide">90.42</td><td class="show_hide">KDGEGAPPA</td><td class="show_hide">1939.90</td><td class="show_hide">77.03</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td></tr>
            <tr class="odd"><td>HLA-DRB1*01:01</td><td>1</td><td>1</td><td>15</td><td class="sequence">GIIGKKDKDGEGAPP</td><td>Consensus (comb.lib./smm/nn)</td><td>90.49</td><td class="show_hide">DKDGEGAPP</td><td class="show_hide">1000000</td><td class="show_hide">89.54</td><td class="show_hide">IIGKKDKDG</td><td class="show_hide">22638</td><td class="show_hide">95.59</td><td class="show_hide">DKDGEGAPP</td><td class="show_hide">4891.40</td><td class="show_hide">90.49</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td><td class="show_hide">-</td></tr>
        '''
        expected_results = [
            ['HLA-DRB1*01:01', '1', '2', '16', 'IIGKKDKDGEGAPPA', 'Consensus (comb.lib./smm/nn)', '84.52', 'KDGEGAPPA', '187971.76', '84.52', 'IIGKKDKDG', '7531', '88.48', 'KDGEGAPPA', '2595.20', '81.51', '-', '-', '-', '-', '-', '-', ],
            ['HLA-DRB1*01:01', '1', '3', '17', 'IGKKDKDGEGAPPAK', 'Consensus (comb.lib./smm/nn)', '84.52', 'KDGEGAPPA', '187971.76', '84.52', 'KDGEGAPPA', '9417', '90.42', 'KDGEGAPPA', '1939.90', '77.03', '-', '-', '-', '-', '-', '-', ],
            ['HLA-DRB1*01:01', '1', '1', '15', 'GIIGKKDKDGEGAPP', 'Consensus (comb.lib./smm/nn)', '90.49', 'DKDGEGAPP', '1000000', '89.54', 'IIGKKDKDG', '22638', '95.59', 'DKDGEGAPP', '4891.40', '90.49', '-', '-', '-', '-', '-', '-', ],
        ]

        html_parser = HTMLTableStripper()
        html_parser.feed(html_results)
        results = html_parser.get_table_contents()
        self.assertEqual(results, expected_results)

    def invalid_html_tests(self):
        bad_html = '<tr></td>'
        html_parser = HTMLTableStripper()
        self.assertRaises(HTMLParseError, html_parser.feed, *[bad_html])
