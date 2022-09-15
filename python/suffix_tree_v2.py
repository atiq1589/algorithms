from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Index:
    value: Optional[int] = None


@dataclass
class TreeNode:
    start_idx: Index
    end_idx: Index
    suffix_link: "TreeNode"
    suffix_start_idx: Optional[Index] = None
    children: Dict[str, "TreeNode"] = field(default_factory=dict)

    @property
    def size(self):
        return self.end_idx.value - self.start_idx.value + 1


@dataclass
class ActivePoint:
    node: TreeNode
    edge: Optional[int] = -1
    length: Optional[int] = 0


class SuffixTree:
    # _TEXT_STOPPER = chr(0)
    _TEXT_STOPPER = '$'

    def __init__(self, text: str):
        text += self._TEXT_STOPPER
        self._text = text
        self._global_end = Index()

        self._tree_root: TreeNode = TreeNode(
            start_idx=Index(None),
            end_idx=self._global_end,
            suffix_link=None,
        )
        self._tree_root.suffix_link = self._tree_root

        self._active_point = ActivePoint(node=self._tree_root)

        self._remaining_suffix = 0

    def _get_current_edge_node(self):
        active_edge_start_str = self._text[self._active_point.edge]
        return self._active_point.node.children[active_edge_start_str]

    def _traverse_edge(self, i):
        edge_node = self._get_current_edge_node()

        if edge_node.size <= self._active_point.length:
            self._active_point.node = edge_node
            self._active_point.edge = edge_node.children[self._text[i]].start_idx.value
            self._active_point.length = self._active_point.length - edge_node.size + 1
        else:
            self._active_point.length += 1

    def _get_next_char(self, i) -> str:
        edge_node = self._get_current_edge_node()
        if edge_node.size == self._active_point.length:
            if self._text[i] in edge_node.children:
                return self._text[i]
            raise KeyError()
        if edge_node.size > self._active_point.length:
            return self._text[self._active_point.edge + self._active_point.length]

        self._active_point.node = edge_node
        self._active_point.length = self._active_point.length - edge_node.size
        self._active_point.edge = self._active_point.edge + edge_node.size
        return self._get_next_char(i)

    def _split_edge(self, i: int) -> TreeNode:
        edge_node = self._get_current_edge_node()
        new_split_edge = TreeNode(
            start_idx=Index(edge_node.start_idx.value),
            end_idx=Index(edge_node.start_idx.value + self._active_point.length - 1),
            suffix_link=self._tree_root,
        )
        new_node = TreeNode(
            start_idx=Index(i),
            end_idx=self._global_end,
            suffix_link=self._tree_root,
        )

        edge_node.start_idx = Index(edge_node.start_idx.value + self._active_point.length)

        new_split_edge.children[self._text[edge_node.start_idx.value]] = edge_node
        new_split_edge.children[self._text[i]] = new_node
        self._active_point.node.children[self._text[new_split_edge.start_idx.value]] = new_split_edge
        return new_split_edge

    def _extension(self, i: int, char: str) -> None:
        self._remaining_suffix += 1
        last_tree_node: TreeNode = None

        while self._remaining_suffix > 0:
            if self._active_point.length == 0:
                if char in self._active_point.node.children:
                    self._active_point.edge = self._active_point.node.children[char].start_idx.value
                    self._active_point.length += 1
                    break
                else:
                    _new_node = TreeNode(start_idx=Index(i), end_idx=self._global_end, suffix_link=self._tree_root)
                    self._active_point.node.children[char] = _new_node
                    self._remaining_suffix -= 1
            else:
                try:
                    nxt_char = self._get_next_char(i)
                    if nxt_char == char:
                        if last_tree_node:
                            last_tree_node.suffix_link = self._get_current_edge_node()
                        self._traverse_edge(i)
                        break

                    new_split_edge = self._split_edge(i)
                    if last_tree_node:
                        last_tree_node.suffix_link = new_split_edge
                    last_tree_node = new_split_edge

                except KeyError:
                    edge_node = self._get_current_edge_node()
                    edge_node.children[char] = TreeNode(
                        start_idx=Index(i),
                        end_idx=self._global_end,
                        suffix_link=self._tree_root,
                    )
                    if last_tree_node:
                        last_tree_node.suffix_link = edge_node
                    last_tree_node = edge_node

                self._remaining_suffix -= 1

                if self._active_point.node != self._tree_root:
                    self._active_point.node = self._active_point.node.suffix_link
                else:
                    self._active_point.edge += 1
                    self._active_point.length -= 1

    def _ukkonen(self):
        for i, char in enumerate(self._text):
            self._global_end.value = i
            self._extension(i, char)

    def search(self, word: str) -> bool:
        _active_edge_start = -1
        _active_node: TreeNode = self._tree_root
        _active_length = 0
        for c in word:
            if _active_length == 0:
                if c not in _active_node.children:
                    return False
                else:
                    _active_node = _active_node.children[c]
                    _active_edge_start = _active_node.start_idx
                    _active_length += 1
            else:
                if self._text[_active_edge_start + _active_length] == c:
                    _active_length += 1
                else:
                    return False
            if _active_edge_start != -1 and _active_edge_start + _active_length - 1 == _active_node.end_idx.value:
                _active_length = 0
        return True

    def printTree(self):
        queue = [(self._tree_root, 0, "Start")]
        print("root")
        prev_level = 0
        while queue:
            node, level, parent = queue.pop(0)
            if prev_level != level:
                prev_level = level
                print()
                print('-' * 100)

            print(parent, end=" => ")

            print("(", node.start_idx.value, ",", node.end_idx.value, end=" ) ")
            print(self._text[node.start_idx.value:node.end_idx.value + 1], end=" " * 4 + "|" * 2 + " " * 4)

            for child in node.children.values():
                queue.append((child, level + 1, node.start_idx.value))
        print()
        print("END")


def dfs(node: TreeNode):
    if not node.children:
        return 1
    res = 0
    for child in node.children.values():
        res += dfs(child)
    return res


def solution(words):
    words.sort(key=len, reverse=True)
    suffix_tree_1 = SuffixTree(words[0])
    suffix_tree_2 = SuffixTree(words[1])
    suffix_tree_1._ukkonen()
    suffix_tree_2._ukkonen()
    for i in range(len(words[-1])):
        for j in range(i + 1):
            if suffix_tree_1.search(words[-1][j:i + 1]) and suffix_tree_2.search(words[-1][j:i + 1]):
                print(words[-1][j:i + 1], len(words[-1][j:i + 1]))
    print(suffix_tree_1.search("cvscxggb"), words[0])
    print(suffix_tree_2.search("cvscxggb"), words[1])


if __name__ == "__main__":
    suffix_instance = SuffixTree("xyzxyaxyb")
    # suffix_instance = SuffixTree("mississi")
    # suffix_instance = SuffixTree("mississiississi")
    # suffix_instance = SuffixTree("banana")
    # suffix_instance = SuffixTree("aaaaa")
    # suffix_instance = SuffixTree("abcdef")
    # suffix_instance = SuffixTree("aladdinaddingdinner")
    # suffix_instance = SuffixTree("fnqduxcvscxggb")
    # suffix_instance = SuffixTree("rfvvrivuly")
    # suffix_instance = SuffixTree("mississipisspis")
    # suffix_instance = SuffixTree("iejieiie")
    # suffix_instance = SuffixTree("ababcabcd")
    # suffix_instance = SuffixTree("abcabxabcd")
    # suffix_instance = SuffixTree("isiii")
    suffix_instance = SuffixTree("ietitietie")

    suffix_instance._ukkonen()
    suffix_instance.printTree()
    print(dfs(suffix_instance._tree_root), len(suffix_instance._text))

    # solution(["fnqduxcvscxggb", "nfcvscxggb", "vsrcvscxggbt"])
    # solution(["aladdin", "adding", "dinner"])

    words = [
        "ietitietie",
        "irrcbjaylbtieucfeoqkqdcyontjoavkhodpwqhwyczxnljfzorqdapocafbiknjzcvvyrbxhpiaqmsszariwcvmjnbwbtrernzkkzujziuysepkzgalnzocexcjwppyzzclvkatnhnstbkktqekoxqijabkrbvixqvsscsmtgbjzannesrblcxbebhorzlgugpihnivgbcsladarecnacxbukemaceyhfyekbxzfdzzsbetmfxazrhxuwmftmjptitwavmrefhzukaocrofyzatjdswzdgxevezikkojjgjackrasqcqdrbtaqwitjbytxxzgtctqouloxomduailksoboctybodtntlorinqightfaicwudbgpkirmvjcjbrsznigxarwrbdsrnriopvrsdrphmdklwvwspacylzabaxvigevnhnnzlkznsyevyavpvqvecmxiylyjuqtxjhzhxkrimngghjenlwnwhtbtvfzurjgutdpqouvjmcaglcgncjrvzesieutjgzgltvrpzccxgjlolyxjkjosngnaytmmsliqmapjelomoemeuhzkltownehhafuklxzfiaexefiqrlhsxvuewmdbsoghbpsqqpbattzeymcujiivggjoaqcgjwidxjufzzwywdcqeykypkzgrwxwxvncgapmgvnbnfkxmkxyoxdvurwlzpjjirkiacwgjejpuzuqrsqanrtizqmejbicgkgrkztbpwqypdifixezkfygoaacicrndrriugosebhxfqgbvujfpjkgxdgtipfbidjuxdkzxdojaujrvaxnfiofwjmezipgiebjevdrzoxijhmgzvlchrbobbhivdwjdlrormareqzzjjxlhkogpmfqsqpsaaeahccgmwfgdtgcjyinwnemyfujwoutwddovdeiktstoomktoepzkpytoiuswhaxcikyapbonwvopylpbjbltqpcrsnzwskjzzzbzselpphuerqkxfsojfrwdbofozpojwmaklatfahadlanpulueoxmidfewnwjeyvpwidssbqramkcvfdwhvycmeutkvzdihxchcowbwhmxbzgiddxhjzxmowtaxudjiawmuppcgvnagruvxcpmfljigntqrshlbafkcvnlhrhjfrmgglnbzpkwgpwyjsiaamxbwqmefefsocfpliijniwmsmspbsmgstpbyhyfrntkexcvkwodhsyjjjtdeivnhwjjsrnpveklryzbxziwyamhijalrbbfbwiknwkjbigllrbpkrnsvtcqxvymexdbzrvwyborszoinafgevnceyjvqinzvtlpzzycfmmemctawdxunqysdymkrqadrbrwdfwiuwcmcdbkcdtrocxqmetvmraiwxgdwnggjdtxethfziqzebzmftlopktjolxxnszqxupjinrtydlkscrgfxvhexpvadajibtmzwaczzmzjidycdymblvnxvvokizbvduedyqrpinluxxiwlwefcmbkrctcozuuzfybfselosjcfbsqsvctlblfojcbycxprvnvrgcxkaxddvtiuifgywcdlrlgusouqnzixogbyqpnvoamsinsjpuhoqtnzrctqbzmbjqcpwdzlvhmbbxxwpxzoicyhkvujrabnqasgybbsimibwkypnlvdcbpsmlvgzwuubapmoaogshuyqkvpukqurscbhfscrrytjawohsqegghvjxnmbcghboqkjzmnvofzpxvwluxviiassqgpsmjntnauqaopourvlgutihscyhasikubvkgbadkjvmonnnlrzrwirrfensjadhoznbnxsokeogaufipdihwubqgbjrfvykogdiiawoxnzsjsixbxfyehgzmqwbvkpjadlzamzafqbqtubkbqtucfexrzcchdjgtngmbelvanpkumsniajnwuaehvcarzjphozngolftuxcceyarhdxysshxkqaokvcovcohvsbainzcisdcxxrbmiyglvwnfsxpokguiultcciraqyntebowyfczkrcimrfwrfqatnbeondptqcbjctbrkznwosoecqtmbjaozbxdjeprvzqitmhwxewxfyqptojgkhsghmbvkybnadcymeyjgdajrvnmbjsnuvpebvghwqqemxgihhpwmycuhnipkppubenikbymvpmuxnxaojthrhooqdnkwkkqthvlcptathtaflypfjchcrufzbfclafngddgemkatwhprcqozcwcgknygzbcdccbkpcdfbhjvyaxcvqdxbqcxmygycgxxxkmgennrgldifptehppleagvapapynhzsqrcnocunbbhuscoobdobhhcpsszxfxhzzorjabrahlygcemmzjgqodknizoaluyekjigdajafkppnhydrfvjwwmwdhaxsoogvbfcgqswzzsfhkulbqfqcfdlwzduprfewoixberujgppduysaxgttgvwhenkqmrnkxoufyiokqitmkeahzxgcfjdkoopmshqdpiyxpfghflpygaegeotdijbysuwwunagkwtgcsnwuzqfrevzuspfgxmawohnkhyqppfnmryicscmivhbfwfbexsojqgoaahynhehjschrqgnnfkqriumabuqmiqwmeglvqnxvpqfodofrezbyoijkgybnarisdhpfaitfojsidcfkmcxsmexsahjnocqarabjtzoyaggcynknhjphmgbkojjbjljucdbsljvylcaimvprjbwtlaxhlscnmmhmtlcxtutuuuggqmdqsapvrfkwzblyhyfynmwbvppbgsvbwpnctifyzpshcofqdphjugeegzqpaougrxroksudhaiasjtsixsozcfkfnhdtgtjgdkkbklmsmmirvqlkddskxzvunyulpijxrskezjtkylawaarrbozlhgvvbaqzcvbmdralhdltheyjuebzjyzaoxgjbkwmdebgpojyishwbtjhijkeatflnoobuzfyigqwbifzddujyxekjiskqnyokcdrxsfshcrsujvoqtjhikgljuvmgrrilofexgqitauzaxgfrbwykndseofkcxtdmzxmsibunthpnptzzflheedftloikliowwknhjfhabdcbtsgrchmygnxwtcwnbkaqqfnkolhjopivklazyfvneoszrpsxkofsomaxdthxsstpjchnvlkuanlshvccydxqntmjhnvjdtdjbfhlaeldmacyzssjorceppbotfyuwkoabailcoronbszestvegujbfvwutanzzklydgwtyeyhavvrziyzlymkvxxxrtmvxkujiirotzflbvxclbqkscvjsxgfrvdzvmtarysjjmlyanupxjpcnvexbwsxvoqxdypqrqdhpiannumpiaxokrhvndtxxfgzoaqzrcyoudvhgmbknctfyvwwqgrudpabviyrouurnvfbfcyvchuiqjuqsflylkufiijwiagrszgananopisdadqgkvpdvjaweomefwmdrbkdfjazrljhjuwkzyxsysmvudiqiwgotqzsavydxzgvwkwuujkqldlqgnjhwsyafugkqenvnmdudyfttgebyuwmisvyphtstatzforpofsbtvhkpazxwzyzxlitmdhksqyhekdppqebyvuzyjufwmsxskxfgkqgbueuqwloyhvltsfoxrhjygzgyhtznyfjwausigkkygjnjegobowkfxqksguamnhyeuasubwogjxwexunwbkfhioqeysjafwyqhslclblehaytxdgrawxjeymwfhlzcsaatximeaglktxdurrwasvsnwdjiatknywttrvispekstmovnegiqwwrqauzhlcuyevvgbglyutmhimwzbeahderwjrrsurfinlcgpstklesgzwvzskhridyjmrxettrqrosaigyrfuqrdduiitgwotyiyppprzehhctbrabztqcrdoreayqkrrstejfohgecokqpxzynqvpmdqcfmduwzdwqoykhsrvcqqrivihihbhuwhpsvdcazeufwfcodbykbzfihqeobnqpojcwxtfqmlspjueitejzuwokctxbdwlknxcxqtbokogxfpirnytofmjfnrwdqiqwyajvfjoopyootrjavmwerhcevzxegqrhqciktcgjwogrqxljqbhmhnbytqkycymdpiwcoljklusxhasyttvadsaoifdvyltqhtvelhbafqfblhqwzpzqhqnpjatrexirxxtjuvcxeyzcaaqrfiardhhmsjgkfpvujfnlzpgvcgxbtpshiqexlmckgigcggdroolitvyjzuqwstfbraawwehhxbbuumshfishwmenzynrnlwmqkytwoynbsntuuahresuqthzzctgnbnuotlreoavjxxzytnntuupxwyqwacgnsehyizksudnaiyemgplxfyrqwcsafriybrjhbhfaffdjjgvavqsammjdyowycbaroggwprztknmltugvsiaihywxkiiwecmayslgpgxoknsknctqghfebifipnwevhuviejmzmbfcktwcudmqwnymdfhuynrssnxccexluuceqoreygwmxxrbnnhhtzidvaglnaabikugaisfmcqdhewlxyjurcbvhmjbnxrrtbltofpqciympmafotkqcbdtwobxkwrdtgsysfuoyoffpdkhsigekhqhtbpymdztyjoftsxutfzzdnqhpbwdfoseaywmjogfqkkzqwvkvdtlyjjokwmdoaskgaqghdfplopeboyodywpjjsjegprprruhemenkgrotszfdheuhxmwjslfdfshxazrmqbnwwtdrwjitaowartswyiudfsnvwdyywuccfjjbbmfogstzvmxzxvbhscbsvzwurxtnoesnejcdgcodirrkoviujgdohqgfkzezxbzgi",
        "dkifwmygdqlwmhybztltebaqfnsfbuuexgdogzoonqggswbgstptlvpcntzpiplxlqfovwmxqnquatgxftxmwtgoevauybyqfposuvnqfmihjslfinmxrpfktlxrwunasnnmcibeaxtygbwpwikrwfppeezetjkobrsbnhiqdfqahorkruzxlxnhuyymxcyjczjidkynbnrusmxlvvdzlnkvlxfplmglaavqlhzdxlehxlpnozhkehjeghmqgjyxyrqquxnzvjnqyzzfbmrstitlkezrupooudqbbsqdqvkxhahkfuveluzjhsvnkgqhtdusyzejvnapekhwmjemlsseohwbvcwjafgurnbagyuqxqqmezlhhprrfakntoplvkcmsczzbinhutjlvtqafrkezvsojocwtcjunebtvcvywhaehhpnxktrfbkeynpuqyrzqvezcesguxtgwzwplzenxbgeazegfivmojiripxihriemtnehbqvezpiprfnxnlaexxtnlhkhvtjjhufgwcsbdelyrjkucburgkdelxxgdptntvktzetyrxmahnithuixwdcfxjvvtltotimheywqlyampfecpefveaipmvenzbdsufogrmpeotczwvdeosbgmgrxupfhivvbqslgmltamsctstxgzwhegrdcupuqqkgekqksdcqrxrlgiwjjoihlahrsqzrwasnmokbngilefshlbuzlcrekmbjvnxcnjfuovsrepuzjkexrfxmoinvgfhibiioixsxufuygkznsmwnquiucfydrbsmimpjmonfobdbnumykrtclciqratbyfwgssoozmpqxhhmhdmighvbbrfltlozsyrjmubnlvoxweeitmmycmvmqmlbrjhoywmsbtdjxcckeynqwqyanvjmvgdpwidoypdckxwhjzibfwwquemqqkjxchzbbegpcjcwpwkulfyflabigbsjktwsgyhaasfctscprqinveuzqylfjpduhwknibxglvecovvtijklqxtvmiurnbowxfnhuyqkfefuqudhbrspdyhfdahpyejivkxndjyjbmxjpcxmvsddkasmlqoejqwgifhgmytwuvgdylotuyjuofjmcgztzmhshnojhkzgenzqyymtjobdyecyivrhxwtjiyickfobufaklnpjaedtizsxgronambzcjzibkfardxydynaepdpdximtiqwkvgpeartzuhttwjyfkikiwcstgheysynjldeocxduxlevrouinkagxuvtgdxrzrsattdwskvgfxqtzaesuvgdkckulteereqqhdxdqgsrmnmthsxknddcgiykrobiobirmisapppoeqektmlzlofjiwzauifiluleirrwzlvxaiugcsbdkeetwfxfozukqrmoxcmzmuqcpvzdibbvmaqcjhxjcknnwgmnftlddbaxbqwjnwkuujebpkeckdrmoisywcfamnevxoxvhzdgffmrarsvgochobscvcpqvemfdjpmywjkhyeqsabnoivxgjdxxsslakdoxiexkppdnrudjzkhackncqqcmolfhasynqasxeappurlrrjcwlcvcpyexskodamxjmbfhbflqvdkgofcajfurnwncydsqseosisbkyolirisdvixqqarjifttnlsxxucelbxbmiaumihuowkryienughakqbkvlqyfjjikixfgajnleglvuqjbwafmxmubhsjkcezpzehiwqcjfpoubrwjklccjvbtqelfpzibeifqhclqvwgpokcbqcybhwfzpyealudeutpxfhyxiotyiksgxwtgyemshuudbaybmayjtzbsbbplpdgmkqagsefiasplwadzfmkyyenncyohuqtjqguwwtmxefdwjefrkblhzmztwyviypjygjlogbogqggkjxuvfmnytrncohjoydblddpysigdxaduofihbaijfkscjcsapzfaspzqbuqmpvwalrzlftgxycergpdxmfbabxsdgxoexgxxmoxxoihikcdefzsvgqzppmegyrqkpxyzbkwodeucgevcxlhuzrleedejmiqgbdbyqqwhqxhubadhungfgcuvkqgmisnclnwlrszbmsudgvttjmusaczeeemlmdowvbtmvlfzlvbfmyofemtniccsxwkbzwlcoupvxqnxcnsgingnkoqcmysrxpavhozmmqipcedvjjdofrypcnhekutsqdukbucyiatfqdjjnhwnlngcnkvcuvtphkqzgeyybxnpktrshypffnowejqmgogesfifrkzovjqzdghjiwcshodbvmcmrokaevtnbvrmelafckzknuswqtwqpqyyviznakngyscpowyjenxdixlpmgjsdobdpkevxpvtvmzuxyxskcuvqzxheqvbqdncwaxmgnqyibqnognptcasjpirtskzvtdtzdhtowzrcfsefbfetapmheaarsguttxwhyjtanbipawaxfvpbmvpzgmqjmtgvepxxjjqolqyccijckjoicsgasdxbzjowqleobpsbevmopahkfrirdecmthiakurdxvyophzpdfetplyghrwnobxnnxfgiazwahcqpregvqmikspbpditipdebveirbiisluwkgwtipudojhblhuorycibrbvbvgqsdafgmtrwetrmvmaemyikpjlhfztchkdcgllofvwodqgpustlejoaywuprrrbpxaqejqxkqozfijsihsoarkhtragldtgrpkucwyjprmgsmnhtguqdgheavumrxkzpuyottypcciphphubugpjntjvrnrsnexxeoovaoqvfvoqyocevbyutxyktjagioqhepeaqsevpdbqauiabyqxquytpsggtxznuternypqfooviojdoilpoitlghplscdqonczbdjwdwtliarknabcswbaugezlioqhbdajqdsvleqqrexqorpkmailawwkwxdmhkflcrqxqbewlkexdyuqbzndwtngrhbtjmenqbwgmigfvffvttngbljxjeflfjiucdzksuslebdconeaulujbkigwwatlxescrwyupapwajhgqzbxwjdavukadllyhbldpnlnydzljdkkikezueuzzljilmodivxtmsodhsboxfrsrilucpyzmpxovpwbbzojfmnjvlnedtfdebnonvvwbhvxsspnqvvzsvbwzpisolwnwdmgaeorgjvqnxjawujxyakdiktyqtofqutwhlckodnajsgnehwduukhzuqzhpyummqlipuhmbbcqlqgaockwnkyuxtbauntabbcpqezobbxezhwhhpmvzohhpbekcvdzhvgquufzfuqkeblcjyyxmzstiqnxgeoigcwrczsqrrkneedpsrieslezfwpwlpbkqmlzpdrtwfvxdajbduffymfyyajcvqsgwqatzmqemscflacpoqquktwcockpqvkemthyzxtgnmhuwletkmqbsakdccwozgryvczclwlnrjugcxqttwioptrzmppqfokpwffybsinwwqkeeuwbgnwtfzmsvibwcywuoeohdfysyanhrvpixcmwbbaylrwxsrdszlvdzdjttwjncdpohjgawzvmrbxkogegkpuhlkknjryjjptmefdqsmndphzxsxcdebzrhscwultlsuhymtacplmjyupudtrulmphegsphxlvekfxeilspjhiknffluzrtrsakepcrdnlohugrvbxohjkdcseufwlsupsvzrvwoizukhvxjsljchzsmpbzltcbsjpoikcutsqmrkmcfvslpddwrsmzlvqakqlbelznxbiubchirnmbnxuzehmwuesllfsgyvsnjgwtjskikgtgkayhlqncosurybeszxrjlancyowkufwervncrlywahvvgynrwtjkmxxljqjmjdibbsuuvmggikznghmvkusuqaailbwjmyxnbufcvxyozflhunrxxtwzdyafnubfesihmuzjsqbcfypobicfgazykbvdeyfphcpozdzfwhfrnwpmcopgfjnlekyewewovdcodfnumfzuaelheieomzygzsduoghhfwrjsoloapmlicxikthdwfgyppfovogyvskarfcubesiwogbxqmagqnvlnwnupgdmhtnetlxoeahsntyeunlmgkbrfpvcstsslialfwbeigvvpkicroqmhnbccgiqcwbvnybhdqcqeucbqcxqniqrhleixzqntxwtibhbazkkpssbkjvmdvwbrvublhnapqtugddtqvqpkjyucrphclzlydzesmjtkzmtmgvziicllbzjlwyemmugbpboqbgjqqjbbcxqdqqfzjbnzsyqiwetdifxgyaodtzpvblmrxzpescefilwbfonkbrbtgpokarpxtekvyhwrcvtaablrbffmqvzxvjsioiyefbgljjnhpuymvdsqhcevsaxhbtrkxejawbeehgrinfaycvrzrdglzomqbizmvxnkunsnbbnjwulctrtgtscnlgdoksrvcgpskaiupohjxoebcitbvxrssaxeyjrpmdjrgvdyfrqoteeepomilrmoaurleswdjusgknawmefymmnvomfcnxgczzqlmtigjqefszfefbtudqofjbffldofbtjehcygeuehnbzpaategslyosvmvlfhnrwnrhpsloamxtqaixqgfrjpovukznoxjvubztygaelzlsadpdrwwvqntpgmugobuhyrwfynueqlywcgpfdfdytgnjgwuyjmnobsgrluiissmjvkaljtmnvnefukuhydwasiarkjkhinmirqolblenvxapccbkgsprcpmtepwssbbtppxiqkfsqcbudygosqhqwsdymllvximffazqphcestdmqaetjofpsclhbxmuqhkajhkrdewugxnkjuntlwrmzpocu",
    ]
    for word in words:
        instance = SuffixTree(word)
        instance._ukkonen()
        print(dfs(instance._tree_root), len(instance._text))
    # SuffixTree(words[0])._ukkonen()
    # SuffixTree(words[1])._ukkonen()
    # SuffixTree(words[2])._ukkonen()
