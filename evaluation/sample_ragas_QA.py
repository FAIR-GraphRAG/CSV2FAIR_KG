sample_ragas_data = [
    {
        "user_input": "What is the biotype of the gene TSPAN6?",
        "retrieved_contexts": [
            "TSPAN6,ENSG00000000003,protein_coding,-,chrX:99883666-99894988,2.93781,2.7836,1.05539978884,0.0777896,0.93295,0.994357,up,7105,T245|TM4SF6|TSPAN-6,MIM:300191|HGNC:HGNC:11858|Ensembl:ENSG00000000003|HPRD:02179,X,Xq22,tetraspanin 6,,GO:0016021(integral component of membrane)//GO:0005887(integral component of plasma membrane)//GO:0070062(extracellular exosome),GO:0004871(signal transducer activity)//GO:0005515(protein binding),GO:1901223(negative regulation of NIK/NF-kappaB signaling)//GO:0039532(negative regulation of viral-induced cytoplasmic pattern recognition receptor signaling pathway)//GO:0007166(cell surface receptor signaling pathway)//GO:0043123(positive regulation of I-kappaB kinase/NF-kappaB signaling)"
        ],
        "response": "",  # Model answer goes here
        "reference": "protein_coding",
    },
    {
        "user_input": "List the synonyms for the gene TNMD.",
        "retrieved_contexts": [
            "TNMD,ENSG00000000005,protein_coding,+,chrX:99839798-99854882,0.449399,0.083861,5.35883724444,2.42192,1,1,up,64102,BRICD4|CHM1L|TEM,MIM:300459|HGNC:HGNC:17757|Ensembl:ENSG00000000005|HPRD:02352|Vega:OTTHUMG00000022001,X,Xq21.33-q23,tenomodulin,,GO:0016021(integral component of membrane)//GO:0005737(cytoplasm)//GO:0005635(nuclear envelope),GO:0005515(protein binding),GO:0071773(cellular response to BMP stimulus)//GO:0001937(negative regulation of endothelial cell proliferation)//GO:0035990(tendon cell differentiation)//GO:0001886(endothelial cell morphogenesis)//GO:0016525(negative regulation of angiogenesis)"
        ],
        "response": "",
        "reference": "BRICD4|CHM1L|TEM",
    },
    {
        "user_input": "What is the fold change for the gene SCYL3?",
        "retrieved_contexts": [
            'SCYL3,ENSG00000000457,protein_coding,-,chr1:169631244-169863408,4.12709,3.35184,1.23129120075,0.300172,0.78845,0.994357,up,57147,PACE-1|PACE1,MIM:608192|HGNC:HGNC:19285|Ensembl:ENSG00000000457|HPRD:07459|Vega:OTTHUMG00000035941,1,1q24.2,"SCY1-like, kinase-like 3",,GO:0005794(Golgi apparatus)//GO:0030027(lamellipodium)//GO:0005737(cytoplasm),GO:0005524(ATP binding)//GO:0004672(protein kinase activity)//GO:0016301(kinase activity)//GO:0005515(protein binding),GO:0006468(protein phosphorylation)//GO:0016477(cell migration)'
        ],
        "response": "",
        "reference": "1.23129120075",
    },
    {
        "user_input": "Which chromosome is the FGR gene located on?",
        "retrieved_contexts": [
            'FGR,ENSG00000000938,protein_coding,-,chr1:27938574-27961788,264.257,119.67,2.20821401261,1.14288,0.2141,0.994357,up,2268,SRC2|c-fgr|c-src2|p55-Fgr|p55c-fgr|p58-Fgr|p58c-fgr,MIM:164940|HGNC:HGNC:3697|Ensembl:ENSG00000000938|HPRD:01288|Vega:OTTHUMG00000003516,1,1p36.2-p36.1,"FGR proto-oncogene, Src family tyrosine kinase",hsa04062(Chemokine signaling pathway)//hsa05169(Epstein-Barr virus infection),GO:0005743(mitochondrial inner membrane)//GO:0070062(extracellular exosome)//GO:0032587(ruffle membrane)//GO:0015629(actin cytoskeleton)//GO:0005886(plasma membrane)//GO:0005829(cytosol)//GO:0005758(mitochondrial intermembrane space)//GO:0031234(extrinsic component of cytoplasmic side of plasma membrane)//GO:0005856(cytoskeleton),GO:0001784(phosphotyrosine binding)//GO:0034988(Fc-gamma receptor I complex binding)//GO:0004713(protein tyrosine kinase activity)//GO:0004715(non-membrane spanning protein tyrosine kinase activity)//GO:0005524(ATP binding)//GO:0034987(immunoglobulin receptor binding)//GO:0019901(protein kinase binding)//GO:0005515(protein binding),GO:0050715(positive regulation of cytokine secretion)//GO:0007169(transmembrane receptor protein tyrosine kinase signaling pathway)//GO:0050830(defense response to Gram-positive bacterium)//GO:0009615(response to virus)//GO:0050764(regulation of phagocytosis)//GO:0014068(positive regulation of phosphatidylinositol 3-kinase signaling)//GO:0038096(Fc-gamma receptor signaling pathway involved in phagocytosis)//GO:0007229(integrin-mediated signaling pathway)//GO:0030335(positive regulation of cell migration)//GO:0045859(regulation of protein kinase activity)//GO:0008360(regulation of cell shape)//GO:0007596(blood coagulation)//GO:0038083(peptidyl-tyrosine autophosphorylation)//GO:0042127(regulation of cell proliferation)//GO:0046777(protein autophosphorylation)//GO:0002768(immune response-regulating cell surface receptor signaling pathway)//GO:0043306(positive regulation of mast cell degranulation)//GO:0045088(regulation of innate immune response)//GO:0045087(innate immune response)//GO:0043552(positive regulation of phosphatidylinositol 3-kinase activity)//GO:0018108(peptidyl-tyrosine phosphorylation)//GO:0006468(protein phosphorylation)//GO:0030154(cell differentiation)'
        ],
        "response": "",
        "reference": "1",
    },
    {
        "user_input": "Give the description of the gene LAS1L.",
        "retrieved_contexts": [
            'LAS1L,ENSG00000001497,protein_coding,-,chrX:64732461-64754655,12.7755,7.43409,1.71850613252,0.781155,0.21655,0.994357,up,81887,Las1-like|dJ475B7.2,MIM:300964|HGNC:HGNC:25726|Ensembl:ENSG00000001497|HPRD:06519|Vega:OTTHUMG00000021720,X,Xq12,"LAS1-like, ribosome biogenesis factor",,GO:0005815(microtubule organizing center)//GO:0005730(nucleolus)//GO:0016020(membrane)//GO:0005654(nucleoplasm)//GO:0071339(MLL1 complex)//GO:0005737(cytoplasm),GO:0044822(poly(A) RNA binding),GO:0006364(rRNA processing)'
        ],
        "response": "",
        "reference": "LAS1-like, ribosome biogenesis factor",
    },
    {
        "user_input": "Which gene among these has the highest fold change between poor and good prognosis groups?",
        "retrieved_contexts": [
            "TSPAN6,ENSG00000000003,protein_coding,-,chrX:99883666-99894988,2.93781,2.7836,1.05539978884,0.0777896,0.93295,0.994357,up,7105,T245|TM4SF6|TSPAN-6,...",
            "TNMD,ENSG00000000005,protein_coding,+,chrX:99839798-99854882,0.449399,0.083861,5.35883724444,2.42192,1,1,up,64102,BRICD4|CHM1L|TEM,...",
            "SCYL3,ENSG00000000457,protein_coding,-,chr1:169631244-169863408,4.12709,3.35184,1.23129120075,0.300172,0.78845,0.994357,up,57147,PACE-1|PACE1,...",
            "FGR,ENSG00000000938,protein_coding,-,chr1:27938574-27961788,264.257,119.67,2.20821401261,1.14288,0.2141,0.994357,up,2268,SRC2|c-fgr|c-src2|p55-Fgr,...",
            "LAS1L,ENSG00000001497,protein_coding,-,chrX:64732461-64754655,12.7755,7.43409,1.71850613252,0.781155,0.21655,0.994357,up,81887,Las1-like|dJ475B7.2,...",
        ],
        "response": "",
        "reference": "TNMD",
    },
    {
        "user_input": "Which pathway is the FGR gene involved in that could be relevant for chemotherapy resistance?",
        "retrieved_contexts": [
            'FGR,ENSG00000000938,protein_coding,-,chr1:27938574-27961788,264.257,119.67,2.20821401261,1.14288,0.2141,0.994357,up,2268,SRC2|c-fgr|c-src2|p55-Fgr|p55c-fgr|p58-Fgr|p58c-fgr,MIM:164940|HGNC:HGNC:3697|Ensembl:ENSG00000000938|HPRD:01288|Vega:OTTHUMG00000003516,1,1p36.2-p36.1,"FGR proto-oncogene, Src family tyrosine kinase",hsa04062(Chemokine signaling pathway)//hsa05169(Epstein-Barr virus infection),GO:0005743(mitochondrial inner membrane)//GO:0070062(extracellular exosome)//GO:0032587(ruffle membrane)//GO:0015629(actin cytoskeleton)//GO:0005886(plasma membrane)//GO:0005829(cytosol)//GO:0005758(mitochondrial intermembrane space)//GO:0031234(extrinsic component of cytoplasmic side of plasma membrane)//GO:0005856(cytoskeleton),GO:0001784(phosphotyrosine binding)//GO:0034988(Fc-gamma receptor I complex binding)//GO:0004713(protein tyrosine kinase activity)//GO:0004715(non-membrane spanning protein tyrosine kinase activity)//GO:0005524(ATP binding)//GO:0034987(immunoglobulin receptor binding)//GO:0019901(protein kinase binding)//GO:0005515(protein binding),GO:0050715(positive regulation of cytokine secretion)//GO:0007169(transmembrane receptor protein tyrosine kinase signaling pathway)//GO:0050830(defense response to Gram-positive bacterium)//GO:0009615(response to virus)//GO:0050764(regulation of phagocytosis)//GO:0014068(positive regulation of phosphatidylinositol 3-kinase signaling)//GO:0038096(Fc-gamma receptor signaling pathway involved in phagocytosis)//GO:0007229(integrin-mediated signaling pathway)//GO:0030335(positive regulation of cell migration)//GO:0045859(regulation of protein kinase activity)//GO:0008360(regulation of cell shape)//GO:0007596(blood coagulation)//GO:0038083(peptidyl-tyrosine autophosphorylation)//GO:0042127(regulation of cell proliferation)//GO:0046777(protein autophosphorylation)//GO:0002768(immune response-regulating cell surface receptor signaling pathway)//GO:0043306(positive regulation of mast cell degranulation)//GO:0045088(regulation of innate immune response)//GO:0045087(innate immune response)//GO:0043552(positive regulation of phosphatidylinositol 3-kinase activity)//GO:0018108(peptidyl-tyrosine phosphorylation)//GO:0006468(protein phosphorylation)//GO:0030154(cell differentiation)'
        ],
        "response": "",
        "reference": "hsa04062(Chemokine signaling pathway)//hsa05169(Epstein-Barr virus infection)",
    },
    {
        "user_input": "Which of the first five genes are associated with the Gene Ontology term 'cell migration', a process relevant to cancer prognosis?",
        "retrieved_contexts": [
            "TSPAN6,ENSG00000000003,protein_coding,-,chrX:99883666-99894988,2.93781,2.7836,...",
            "TNMD,ENSG00000000005,protein_coding,+,chrX:99839798-99854882,0.449399,0.083861,...",
            "SCYL3,ENSG00000000457,protein_coding,-,chr1:169631244-169863408,4.12709,3.35184,...",
            "FGR,ENSG00000000938,protein_coding,-,chr1:27938574-27961788,264.257,119.67,...",
            "LAS1L,ENSG00000001497,protein_coding,-,chrX:64732461-64754655,12.7755,7.43409,...",
        ],
        "response": "",
        "reference": "SCYL3",
    },
]
