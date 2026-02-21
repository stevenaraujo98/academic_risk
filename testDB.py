from dotenv import load_dotenv
load_dotenv()
import os
os.add_dll_directory('C:\\Program Files\\IBM\\SQLLIB\\BIN')

import ibm_db

# Conexión
conn_str = 'DATABASE=SAAC;HOSTNAME=192.168.254.53;PORT=50000;PROTOCOL=TCPIP;UID=usrotri;PWD=' + os.getenv('PASSWORD_TESTDB') + ';'
conn = ibm_db.connect(conn_str, '', '')

# Query directo (escapando comillas simples si es necesario)
query = """
SELECT * FROM SOTRI.T_OTRI_PI_RESPUESTA topr;
"""

result = ibm_db.exec_immediate(conn, query)
row = ibm_db.fetch_assoc(result)
while row:
    print(row)
    row = ibm_db.fetch_assoc(result)

print("*"*100)
task_id = "66842604-0e85-4bfe-9196-1a2d42bbcbf3"
query_get_id_proceso = "SELECT IDOTRIPIPROCESO FROM SOTRI.T_OTRI_PI_PROCESO WHERE IDTAREA = ?"
stmt = ibm_db.prepare(conn, query_get_id_proceso)
ibm_db.execute(stmt, (task_id,))
row = ibm_db.fetch_assoc(stmt)
print("Row fetched for task_id:", row)
id_proceso = row['IDOTRIPIPROCESO'] if row else None

if not id_proceso:
    raise Exception(f"No se encontró proceso para task_id: {task_id}")
print("ID Proceso obtenido:", id_proceso)


import json
import datetime as dt
import re

def get_id_inserted(conn):
    stmt_id = ibm_db.exec_immediate(conn, "VALUES IDENTITY_VAL_LOCAL()")
    row = ibm_db.fetch_tuple(stmt_id)
    return row[0] if row else None



report = {
    "timestamp": dt.datetime.now(dt.UTC).isoformat(),
    "top_references": [
            {
                "source": "scopus",
                "id": "85058565410",
                "title": "Reducing the Gap between the Activation Energy Measured in the Liquid and the Glassy States by Adding a Plasticizer to Polylactide",
                "date": "2018-12-12",
                "url": "https://doi.org/10.1021/acsomega.8b02474",
                "score": 0.9867,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Steven Araujo, Nicolas Delpouve, Alexandre Dhotel, Sandra Domenek, Alain Guinault, Laurent Delbreilh, Eric Dargent",
                "abstract": "The kinetic fragility of a glass-forming liquid is an important parameter to describe its molecular mobility. In most polymers, the kinetic fragility index obtained from the glassy state by thermally stimulated depolarization current is lower than the one determined in the liquid-like state by dielectric relaxation spectroscopy, as shown in this work for neat polylactide (PLA). When PLA is plasticized to different extents, the fragility calculated in the liquid-like state progressively decreases, until approaching the value of fragility calculated from the glass, which on the other hand remains constant with plasticization. Using the cooperative rearranging region (CRR) concept, it is shown that the decrease of the fragility in the liquid-like state is concomitant with a decrease of the cooperativity length. By splitting the fragility calculated in the liquid, in two contributions: volume and energetic, respectively, dependent and independent on cooperativity, we observed that the slope of the fragility plot in the glass is equivalent to the energetic contribution of the fragility in the liquid. It is then deduced that the difference between the slopes of the relaxation time dependence calculated in both glass and liquid is an indicator of the cooperative character of the segmental relaxation when transiting from liquid to glass. As the main structural consequence of plasticization lies in the decrease of interchain weak bonds, it is assumed that these bonds drive the size of the CRR. In contrast, the dynamics in the glass are independent on plasticization structural effects."
            },
            {
                "source": "pubmed",
                "id": "31458329",
                "title": "Reducing the Gap between the Activation Energy Measured in the Liquid and the Glassy States by Adding a Plasticizer to Polylactide.",
                "date": "2018 Dec 31",
                "url": "https://pubmed.ncbi.nlm.nih.gov/31458329/",
                "score": 0.9746,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Steven Araujo, Nicolas Delpouve, Alexandre Dhotel, Sandra Domenek, Alain Guinault, Laurent Delbreilh, Eric Dargent",
                "abstract": "The kinetic fragility of a glass-forming liquid is an important parameter to describe its molecular mobility. In most polymers, the kinetic fragility index obtained from the glassy state by thermally stimulated depolarization current is lower than the one determined in the liquid-like state by dielectric relaxation spectroscopy, as shown in this work for neat polylactide (PLA). When PLA is plasticized to different extents, the fragility calculated in the liquid-like state progressively decreases, until approaching the value of fragility calculated from the glass, which on the other hand remains constant with plasticization. Using the cooperative rearranging region (CRR) concept, it is shown that the decrease of the fragility in the liquid-like state is concomitant with a decrease of the cooperativity length. By splitting the fragility calculated in the liquid, in two contributions: volume and energetic, respectively, dependent and independent on cooperativity, we observed that the slope of the fragility plot in the glass is equivalent to the energetic contribution of the fragility in the liquid. It is then deduced that the difference between the slopes of the relaxation time dependence calculated in both glass and liquid is an indicator of the cooperative character of the segmental relaxation when transiting from liquid to glass. As the main structural consequence of plasticization lies in the decrease of interchain weak bonds, it is assumed that these bonds drive the size of the CRR. In contrast, the dynamics in the glass are independent on plasticization structural effects."
            },
            {
                "source": "wos",
                "id": "WOS:000454244600078",
                "title": "Reducing the Gap between the Activation Energy Measured in the Liquid and the Glassy States by Adding a Plasticizer to Polylactide",
                "date": "2018-12",
                "url": "https://doi.org/10.1021/acsomega.8b02474",
                "score": 0.8277,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Araujo, Steven, Delpouve, Nicolas, Dhotel, Alexandre, Domenek, Sandra, Guinault, Alain, Delbreilh, Laurent, Dargent, Eric",
                "abstract": ""
            },
            {
                "source": "scopus",
                "id": "85210300296",
                "title": "Study of PVAc/EVA polymer series: Influence of the inter-/intra-molecular interaction ratio on the molecular mobility at the glass transition",
                "date": "2024-11-28",
                "url": "https://doi.org/10.1063/5.0233715",
                "score": 0.7683,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Jules Trubert, Liubov Matkovska, Allisson Saiter-Fourcin, Laurent Delbreilh",
                "abstract": "In this work, the molecular mobility at the glass transition of poly(vinyl acetate) (PVAc) and poly(ethylene-co-vinyl acetate) (EVA) amorphous sample series was investigated. The temperature and pressure dependences of the intermolecular interactions were studied from time-temperature-pressure superpositions and from the relaxation time dispersion of the segmental relaxation. The difference in terms of intermolecular interactions due to the lateral group ratio of vinyl acetate (VAc) was then estimated from the activation volume and related to the cooperative behavior. The isobaric fragility and its two contributions (thermal and volumetric) were estimated through high pressure broadband dielectric spectroscopy measurements. The volumetric and thermal contributions show different behaviors as a function of the VAc ratio and as a function of the pressure. Thus, the study of the PVAc/EVA series has allowed us to emphasize that the intramolecular and intermolecular interactions induced by the dipolar pendant groups directly influence the thermal and volumetric contributions to the isobaric fragility."
            },
            {
                "source": "scopus",
                "id": "85183793425",
                "title": "Highlighting the interdependence between volumetric contribution of fragility and cooperativity for polymeric segmental relaxation",
                "date": "2024-01-28",
                "url": "https://doi.org/10.1063/5.0187941",
                "score": 0.7646,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Jules Trubert, Liubov Matkovska, Allisson Saiter-Fourcin, Laurent Delbreilh",
                "abstract": "The blurring around the link between the isobaric fragility and the characteristic size of cooperative rearranging region for glass-forming liquids has been cleared up by considering volumetric and thermal contributions of the structural relaxation. The measurement of these contributions is carried out for three amorphous thermoplastic polymers using broadband dielectric spectroscopy under pressure, providing an understanding of the link between isobaric fragilities, glass transition temperatures, and microstructures. The cooperative rearranging region (CRR) volume is calculated as a function of pressure using the extended Donth\u2019s approach, and the values are compared with the activation volume at the glass transition under different isobaric conditions. By combining these different results, a link between the chemical structure and the influence of pressure/temperature on the molecular mobility can be established. Furthermore, this study shows also a strong correlation between the activation volume, leading to the volumetric contribution of the isobaric fragility, and the CRR volume. Finally, this work highlights the influence of inter- and intra-molecular interactions on thermal and volumetric contributions of the isobaric fragility as a function of pressure."
            },
            {
                "source": "scopus",
                "id": "85082171680",
                "title": "Amorphous rigidification and cooperativity drop in semi\u2212crystalline plasticized polylactide",
                "date": "2020-04-24",
                "url": "https://doi.org/10.1016/j.polymer.2020.122373",
                "score": 0.7529,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Varol, Delpouve, Araujo, Domenek, Guinault, Golovchak, Ingram, Delbreilh, Dargent",
                "abstract": "Plasticization of amorphous polylactide shifts the glass transition and extends its temperature range of crystallization to lower temperatures. In this work, we focus on how low\u2212temperature crystallization impacts the mobility of the amorphous phase. Plasticizer accumulates in the amorphous phase because it is excluded from the growing crystal. The formation of rigid amorphous fraction is favored by the low crystallization temperature. It reaches values up to 50% in plasticized polylactide. The increase in the content of rigid amorphous fraction coincides with both the increase of free volume quantified by positron annihilation lifetime spectroscopy, and the decrease in the cooperativity length obtained from the temperature fluctuation approach. The drop of cooperativity is interpreted in terms of mobility gradient due to the amorphous rigidification."
            },
            {
                "source": "scopus",
                "id": "85087069557",
                "title": "Antiplasticization of polymer materials: Structural aspects and effects on mechanical and diffusion-controlled properties",
                "date": "2020-04-01",
                "url": "https://doi.org/10.3390/POLYM12040769",
                "score": 0.69,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Leno Mascia, Yannis Kouparitsas, Davide Nocita, Xujin Bao",
                "abstract": "Antiplasticization of glassy polymers, arising from the addition of small amounts of plasticizer, was examined to highlight the developments that have taken place over the last few decades, aiming to fill gaps of knowledge in the large number of disjointed publications. The analysis includes the role of polymer/plasticizer molecular interactions and the conditions leading to the cross-over from antiplasticization to plasticization. This was based on molecular dynamics considerations of thermal transitions and related relaxation spectra, alongside the deviation of free volumes from the additivity rule. Useful insights were gained from an analysis of data on molecular glasses, including the implications of the glass fragility concept. The effects of molecular packing resulting from antiplasticization are also discussed in the context of physical ageing. These include considerations on the effects on mechanical properties and diffusion-controlled behaviour. Some peculiar features of antiplasticization regarding changes in Tg were probed and the effects of water were examined, both as a single component and in combination with other plasticizers to illustrate the role of intermolecular forces. The analysis has also brought to light the shortcomings of existing theories for disregarding the dual cross-over from antiplasticization to plasticization with respect to modulus variation with temperature and for not addressing failure related properties, such as yielding, crazing and fracture toughness."
            },
            {
                "source": "scopus",
                "id": "85071027353",
                "title": "Cooperativity Scaling and Free Volume in Plasticized Polylactide",
                "date": "2019-08-27",
                "url": "https://doi.org/10.1021/acs.macromol.9b00464",
                "score": 0.6736,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Steven Araujo, Nicolas Delpouve, Sandra Domenek, Alain Guinault, Roman Golovchak, Roman Szatanik, Adam Ingram, Cyrille Fauchard, Laurent Delbreilh, Eric Dargent",
                "abstract": "The experimental evidence of the increase of activation energy associated with the super Arrhenius behavior governing amorphous polylactide by free volume variations has been obtained through a combination of calorimetric, dielectric, and positron annihilation lifetime measurements. The amount of free volume in polylactide was controlled by the amount of acetyltributylcitrate plasticizer in the composition. Plasticization is shown to decrease both the fragility index and the scale of cooperative motions at the glass transition. The calculations of volume and energetic components of kinetic fragility reveal that the fragility drop is governed by the change in the size of cooperative rearranging region. As a result, direct correlation has been established between cooperativity and activation energy for the entire plasticized polylactide series. It is also shown that cooperativity variations with both temperature and plasticizer content can be simplified as a master curve with free volume."
            },
            {
                "source": "scopus",
                "id": "85133551319",
                "title": "Segmental Relaxation Dynamics in Amorphous Polylactide Exposed to UV Light",
                "date": "2022-08-01",
                "url": "https://doi.org/10.1002/macp.202200085",
                "score": 0.6662,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Steven Araujo, Chlo\u00e9 Sainlaud, Nicolas Delpouve, Emmanuel Richaud, Laurent Delbreilh, Eric Dargent",
                "abstract": "The degradation of polylactide (PLA) under UV exposure is investigated in terms of cooperativity and kinetic fragility at the glass transition. In the first part, possibly coexisting degradation mechanisms are evoked from the interpretation of the infrared spectroscopy analyses. Furthermore, the reduction of PLA chain length, owing to photolytic scissions predominant over local crosslinks, is assessed from chromatography, and confirmed by the shift of the glass transition temperature toward lower temperature. Modulated temperature thermogravimetric analysis (MT-TGA) also shows that the activation energy needed to initiate thermal degradation falls after UV exposure. In the second part, the impact of UV-induced degradation on the cooperative rearranging region (CRR) size and the kinetic fragility, respectively, calculated thanks to calorimetric and dielectric measurements, is discussed. Despite the assumed concomitance of several degradation mechanisms, it is observed that the glass transition, the kinetic fragility, and the CRR size decrease together with the exposure time. Moreover, it is found that the data align well on another trend depicting the change in the relaxation properties caused by plasticization of PLA. Thus, the variations of segmental relaxation properties caused by UV may be related to the increase of free volume linked to the damaging of the PLA structure."
            },
            {
                "source": "scopus",
                "id": "85178091542",
                "title": "How temperature-induced depolymerization and plasticization affect the process of structural relaxation",
                "date": "2024-01-05",
                "url": "https://doi.org/10.1016/j.polymer.2023.126549",
                "score": 0.6642,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Roman Svoboda, Jana Machotov\u00e1, \u0160t\u011bp\u00e1n Podzimek, Pavla Honcov\u00e1, Maria Chrom\u010d\u00edkov\u00e1, Martina Nalezinkov\u00e1, Jan Loskot, Ale\u0161 Bezrouk, Daniel Jezbera",
                "abstract": "The self-plasticization, i.e., the increase in the polymer segmental mobility by the inclusion of its own monomer, has a major impact on the structural, thermal, and mechanical properties of the polymer. Differential scanning calorimetry (DSC) was used to investigate the influence of thermally induced self-plasticization on the structural relaxation of polydioxanone (PDX). Depolymerization (based dominantly on the end-chain scission mechanism) was found to be controlled by the depolymerization temperature Td as well as the actual number of re-melting cycles (while keeping the time spent at Td constant). PDX samples with the glass transition temperature (Tg) ranging from \u221252 (highly plasticized) to \u221213 \u00b0C (virgin) were prepared. The DSC data were described in terms of the Tool-Narayanaswamy model; a consistent structural relaxation behavior associating the degree of plasticization with Tg was identified. The activation energy first decreased with plasticization from 430 kJ mol\u22121 to 210 kJ mol\u22121 in the Tg range of \u221240 to \u221213C, which is consistent with the plasticization-caused spacing-apart of the polymer chains resulting in larger free volume and increased freedom for the relaxation movements. For the highly plasticized PDX samples, the activation energy increased from 210 kJ mol\u22121 to 310 kJ mol\u22121, which appears to be associated with the possible segregation of the portion of the plasticizer into a discrete phase. The width of the relaxation times distribution increased with plasticization as a consequence of the plasticizer loosening the polymeric chains and enabling a wider variety of the segmental movement. The plasticization also leads to a higher dependence of the segmental relaxation movements on their current physico-chemical and steric surrounding."
            },
            {
                "source": "scopus",
                "id": "85078349470",
                "title": "A simple mean-field model of glassy dynamics and glass transition",
                "date": "2020-01-01",
                "url": "https://doi.org/10.1039/c9sm01575b",
                "score": 0.6317,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Valeriy V. Ginzburg",
                "abstract": "We propose a phenomenological model to describe the equilibrium dynamic behavior of amorphous glassy materials. It is assumed that a material can be represented by a lattice of cooperatively re-arranging regions (CRRs), with each CRR having two states, the low-temperature \"solid\" and the high-temperature \"liquid\". At low temperatures, the material exhibits two characteristic relaxation times, corresponding to the slow large-scale motion between the \"solid\" CRRs (\u03b1-relaxation) and the faster local motion within individual CRRs (\u03b2-relaxation). At high temperatures, the \u03b1- and \u03b2-relaxation times merge, as observed experimentally and suggested by the \"Coupling Model\" framework. Our new approach is labeled \"Two-state, two (time)scale model\" or TS2. It is shown that the TS2 treatment can successfully describe the \"two-Arrhenius\" relaxation time behavior described in several recent experiments. We also apply TS2 to describe the pressure- and molecular-weight dependence of the glass transition temperature in bulk polymers, as well as its dependence on film thickness in thin films."
            },
            {
                "source": "scopus",
                "id": "85068762283",
                "title": "Dielectric and calorimetric signatures of chain orientation in strong and tough ultrafine electrospun polyacrylonitrile",
                "date": "2019-09-12",
                "url": "https://doi.org/10.1016/j.polymer.2019.121638",
                "score": 0.6165,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Steven Araujo, Nicolas Delpouve, Laurent Delbreilh, Dimitry Papkov, Dzenis, Eric Dargent",
                "abstract": "Ultrafine diameter fibers of polyacrylonitrile (PAN), obtained from electrospinning, have huge potential for structural applications since they exhibit an unusual combination of strength and toughness. However, the difficulty to characterize their supramolecular architecture limits their production at the industrial scale. In this work, the glass transition of electrospun nanofiber mats of PAN was investigated by means of thermal analysis techniques. Modulated temperature differential scanning calorimetry (MT\u2013DSC) and dielectric relaxation spectroscopy (DRS) were used, and relaxation parameters characteristic of the glass transition were obtained. Reduction in average fiber diameter resulted in broadening of the glass transition and a shift of its midpoint to higher temperatures as observed by MT\u2013DSC, revealing additional level of constraints in the amorphous phase. The DRS curves, obtained above the calorimetric signature of the glass transition, superimpose independently on the fiber diameter. This result, which contrasts with MT\u2013DSC observations, shows that the constraint of mobility evidenced at the glass transition, is suppressed when driving the fiber mat to higher temperatures. The dielectric strength increases with temperature, revealing an increase in the density of dipoles participating to the relaxation dynamics. This result, commonly attributed to the progressive mobilization of initially constrained amorphous phase, supports the hypothesis that electrospinning process induces higher level of polymer chain orientation at small fiber diameters, which fades away when crossing the glass transition. The orientation impacts the temperature dependence of the relaxation time close to the glass transition, as it shows higher deviation from Arrhenius behavior with the decrease of the fiber diameter. This leads to an increase of the fragility index which comes in opposition to the decrease in the cooperativity length, estimated from the temperature fluctuation approach of the cooperative rearranging region (CRR) concept. To explain this result, both volume and thermal contributions of the fragility index have been calculated, and a strong increase in the thermal contribution has been observed for the most oriented material. This result is interpreted as a signature of an increase in the polymer chain rigidity."
            },
            {
                "source": "eric",
                "id": "EJ348017",
                "title": "Introducing Plastics in the Laboratory: Synthesis of a Plasticizer, Dioctylphthalate and Evaluation of its Effects on the Physical Properties of Polystyrenes.",
                "date": "1986",
                "url": "https://eric.ed.gov/?id=EJ348017",
                "score": 0.591,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Caspar, A., And Others",
                "abstract": "Proposes a two-stage experimental approach that combines preparative chemistry and polymer characterization. Describes the simple organic synthesis of a plasticizer, the dioctylphthalate, and its direct use in the preparation of a styrene/divinylbenzene network copolymer. Discusses how to evaluate the physical properties of the resulting plastic. (TW)\n\nType: Journal Articles, Guides - Classroom - Teacher | Language: English | Peer Reviewed"
            },
            {
                "source": "scopus",
                "id": "85097139614",
                "title": "Molecular mobility in amorphous biobased copolyesters obtained with 2,5- and 2,4-furandicarboxylate acid",
                "date": "2021-01-20",
                "url": "https://doi.org/10.1016/j.polymer.2020.123225",
                "score": 0.5899,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Aur\u00e9lie Bourdet, Steven Araujo, Shanmugam Thiyagarajan, Laurent Delbreilh, Antonella Esposito, Eric Dargent",
                "abstract": "Poly(ethylene 2,5-furandicarboxylate) (2,5-PEF) is one of the most credible biobased alternative to poly (ethylene terephthalate) (PET). The Henkel disproportionation reaction that leads to furandicarboxylic acid (FDCA) provides three position isomers: 2,5-FDCA (obtained with the highest yield), 2,4-FDCA (so far considered as a by-product), and 3,4-FDCA (traces). The copolymerization of the two main isomers of FDCA with a diol, e.g. ethylene glycol (EG), is an interesting approach to obtain a family of furan-based biopolymers with adjusted physical properties. This work investigates the molecular mobility of three copolymers obtained with EG and ratios of 2,5-FDCA and 2,4-FDCA ensuring the complete disruption of crystallization (90:10, 85:15 and 50:50 mol % of 2,5:2,4 FDCA), as compared to the homopolymers 2,5-PEF and 2,4-PEF. The molecular mobility was investigated by cross-comparing the results obtained by Modulated-Temperature Differential Scanning Calorimetry (MT-DSC), Dielectric Relaxation Spectroscopy (DRS) and Thermo-Stimulated Depolarization Currents (TSDC), with the aim of evaluating the local and segmental molecular mobilities, their activation energies, as well as the temperature dependence of the relaxation time and of the cooperatively rearranging regions at the glass transition. The furan ring in 2,5-FDCA (2,5-PEF) has a rotation axis that is less linear compared to the benzene ring in terephthalic acid (PET), with consequences on the ring-flipping mechanisms. 2,5-FDCA and 2,4-FDCA differ by the position of the carbonyl groups on the furan ring, which adds asymmetry to non-linearity. The incorporation of 2,4-FDCA-based units into a polymer backbone mainly constituted of 2,5-FDCA-based repeating units is responsible for longer relaxation times associated with the local \u03b2 relaxation processes, no striking effects on the kinetic fragility index m, no obvious effects on cooperativity (a slightly increase in the cooperativity length is observed in the liquid state), no effects on the activation energy for the segmental \u03b1 relaxation in the liquid state, and a decrease in the activation energy in the glassy state."
            },
            {
                "source": "scopus",
                "id": "85082765328",
                "title": "Distinct dynamics of structural relaxation in the amorphous phase of poly(l-lactic acid) revealed by quiescent crystallization",
                "date": "2020-04-07",
                "url": "https://doi.org/10.1039/c9sm02541c",
                "score": 0.5795,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Xavier Monnier, Nicolas Delpouve, Allisson Saiter-Fourcin",
                "abstract": "Fast scanning calorimetry (FSC) experiments were performed to investigate physical aging in amorphous and semi-crystalline poly(l-lactic acid)s (PLLAs) that were thermally crystallized under conditions leading to the \u03b1\u2032- or \u03b1-crystalline form, and either favouring or inhibiting the development of a rigid amorphous fraction (RAF). The enthalpy of recovery was calculated after two procedures of rescaling to the content of the whole amorphous phase and also to the only content of the mobile amorphous fraction (MAF), which helped in clarifying the contribution of the RAF. From the dependence of the structural relaxation rate on the aging temperature, two regimes were evidenced for all samples. In the aging temperature domain situated close to the glass transition, the structural relaxation occurs significantly faster in the MAF. Its rate is independent of the aging temperature and is not influenced by the microstructure. However, the distance to equilibrium is higher in samples for which the coupling is strong between crystal and amorphous, implying that the time to reach equilibrium is also higher. In contrast, at low aging temperatures, for which the whole amorphous phase can be considered as solid, MAF and RAF exhibit the same structrural relaxation rate. This convergence in the relaxation kinetics by decreasing the temperature of physical aging was interpreted as the evolution of relaxation dynamics in the MAF from segmental to local. This change is highlighted by the comparison between MAF and RAF relaxation kinetics, but it occurs similarly in a pure amorphous system."
            }
        ],
    "top_references_articles": [
        {
            "source": "scopus",
            "id": "85058565410",
            "title": "Reducing the Gap between the Activation Energy Measured in the Liquid and the Glassy States by Adding a Plasticizer to Polylactide",
            "date": "2018-12-12",
            "url": "https://doi.org/10.1021/acsomega.8b02474",
            "score": 0.9867,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Steven Araujo, Nicolas Delpouve, Alexandre Dhotel, Sandra Domenek, Alain Guinault, Laurent Delbreilh, Eric Dargent",
            "abstract": "The kinetic fragility of a glass-forming liquid is an important parameter to describe its molecular mobility. In most polymers, the kinetic fragility index obtained from the glassy state by thermally stimulated depolarization current is lower than the one determined in the liquid-like state by dielectric relaxation spectroscopy, as shown in this work for neat polylactide (PLA). When PLA is plasticized to different extents, the fragility calculated in the liquid-like state progressively decreases, until approaching the value of fragility calculated from the glass, which on the other hand remains constant with plasticization. Using the cooperative rearranging region (CRR) concept, it is shown that the decrease of the fragility in the liquid-like state is concomitant with a decrease of the cooperativity length. By splitting the fragility calculated in the liquid, in two contributions: volume and energetic, respectively, dependent and independent on cooperativity, we observed that the slope of the fragility plot in the glass is equivalent to the energetic contribution of the fragility in the liquid. It is then deduced that the difference between the slopes of the relaxation time dependence calculated in both glass and liquid is an indicator of the cooperative character of the segmental relaxation when transiting from liquid to glass. As the main structural consequence of plasticization lies in the decrease of interchain weak bonds, it is assumed that these bonds drive the size of the CRR. In contrast, the dynamics in the glass are independent on plasticization structural effects."
        },
        {
            "source": "pubmed",
            "id": "31458329",
            "title": "Reducing the Gap between the Activation Energy Measured in the Liquid and the Glassy States by Adding a Plasticizer to Polylactide.",
            "date": "2018 Dec 31",
            "url": "https://pubmed.ncbi.nlm.nih.gov/31458329/",
            "score": 0.9746,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Steven Araujo, Nicolas Delpouve, Alexandre Dhotel, Sandra Domenek, Alain Guinault, Laurent Delbreilh, Eric Dargent",
            "abstract": "The kinetic fragility of a glass-forming liquid is an important parameter to describe its molecular mobility. In most polymers, the kinetic fragility index obtained from the glassy state by thermally stimulated depolarization current is lower than the one determined in the liquid-like state by dielectric relaxation spectroscopy, as shown in this work for neat polylactide (PLA). When PLA is plasticized to different extents, the fragility calculated in the liquid-like state progressively decreases, until approaching the value of fragility calculated from the glass, which on the other hand remains constant with plasticization. Using the cooperative rearranging region (CRR) concept, it is shown that the decrease of the fragility in the liquid-like state is concomitant with a decrease of the cooperativity length. By splitting the fragility calculated in the liquid, in two contributions: volume and energetic, respectively, dependent and independent on cooperativity, we observed that the slope of the fragility plot in the glass is equivalent to the energetic contribution of the fragility in the liquid. It is then deduced that the difference between the slopes of the relaxation time dependence calculated in both glass and liquid is an indicator of the cooperative character of the segmental relaxation when transiting from liquid to glass. As the main structural consequence of plasticization lies in the decrease of interchain weak bonds, it is assumed that these bonds drive the size of the CRR. In contrast, the dynamics in the glass are independent on plasticization structural effects."
        },
        {
            "source": "wos",
            "id": "WOS:000454244600078",
            "title": "Reducing the Gap between the Activation Energy Measured in the Liquid and the Glassy States by Adding a Plasticizer to Polylactide",
            "date": "2018-12",
            "url": "https://doi.org/10.1021/acsomega.8b02474",
            "score": 0.8277,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Araujo, Steven, Delpouve, Nicolas, Dhotel, Alexandre, Domenek, Sandra, Guinault, Alain, Delbreilh, Laurent, Dargent, Eric",
            "abstract": ""
        },
        {
            "source": "scopus",
            "id": "85210300296",
            "title": "Study of PVAc/EVA polymer series: Influence of the inter-/intra-molecular interaction ratio on the molecular mobility at the glass transition",
            "date": "2024-11-28",
            "url": "https://doi.org/10.1063/5.0233715",
            "score": 0.7683,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Jules Trubert, Liubov Matkovska, Allisson Saiter-Fourcin, Laurent Delbreilh",
            "abstract": "In this work, the molecular mobility at the glass transition of poly(vinyl acetate) (PVAc) and poly(ethylene-co-vinyl acetate) (EVA) amorphous sample series was investigated. The temperature and pressure dependences of the intermolecular interactions were studied from time-temperature-pressure superpositions and from the relaxation time dispersion of the segmental relaxation. The difference in terms of intermolecular interactions due to the lateral group ratio of vinyl acetate (VAc) was then estimated from the activation volume and related to the cooperative behavior. The isobaric fragility and its two contributions (thermal and volumetric) were estimated through high pressure broadband dielectric spectroscopy measurements. The volumetric and thermal contributions show different behaviors as a function of the VAc ratio and as a function of the pressure. Thus, the study of the PVAc/EVA series has allowed us to emphasize that the intramolecular and intermolecular interactions induced by the dipolar pendant groups directly influence the thermal and volumetric contributions to the isobaric fragility."
        },
        {
            "source": "scopus",
            "id": "85183793425",
            "title": "Highlighting the interdependence between volumetric contribution of fragility and cooperativity for polymeric segmental relaxation",
            "date": "2024-01-28",
            "url": "https://doi.org/10.1063/5.0187941",
            "score": 0.7646,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Jules Trubert, Liubov Matkovska, Allisson Saiter-Fourcin, Laurent Delbreilh",
            "abstract": "The blurring around the link between the isobaric fragility and the characteristic size of cooperative rearranging region for glass-forming liquids has been cleared up by considering volumetric and thermal contributions of the structural relaxation. The measurement of these contributions is carried out for three amorphous thermoplastic polymers using broadband dielectric spectroscopy under pressure, providing an understanding of the link between isobaric fragilities, glass transition temperatures, and microstructures. The cooperative rearranging region (CRR) volume is calculated as a function of pressure using the extended Donth\u2019s approach, and the values are compared with the activation volume at the glass transition under different isobaric conditions. By combining these different results, a link between the chemical structure and the influence of pressure/temperature on the molecular mobility can be established. Furthermore, this study shows also a strong correlation between the activation volume, leading to the volumetric contribution of the isobaric fragility, and the CRR volume. Finally, this work highlights the influence of inter- and intra-molecular interactions on thermal and volumetric contributions of the isobaric fragility as a function of pressure."
        },
        {
            "source": "scopus",
            "id": "85082171680",
            "title": "Amorphous rigidification and cooperativity drop in semi\u2212crystalline plasticized polylactide",
            "date": "2020-04-24",
            "url": "https://doi.org/10.1016/j.polymer.2020.122373",
            "score": 0.7529,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Varol, Delpouve, Araujo, Domenek, Guinault, Golovchak, Ingram, Delbreilh, Dargent",
            "abstract": "Plasticization of amorphous polylactide shifts the glass transition and extends its temperature range of crystallization to lower temperatures. In this work, we focus on how low\u2212temperature crystallization impacts the mobility of the amorphous phase. Plasticizer accumulates in the amorphous phase because it is excluded from the growing crystal. The formation of rigid amorphous fraction is favored by the low crystallization temperature. It reaches values up to 50% in plasticized polylactide. The increase in the content of rigid amorphous fraction coincides with both the increase of free volume quantified by positron annihilation lifetime spectroscopy, and the decrease in the cooperativity length obtained from the temperature fluctuation approach. The drop of cooperativity is interpreted in terms of mobility gradient due to the amorphous rigidification."
        },
        {
            "source": "scopus",
            "id": "85087069557",
            "title": "Antiplasticization of polymer materials: Structural aspects and effects on mechanical and diffusion-controlled properties",
            "date": "2020-04-01",
            "url": "https://doi.org/10.3390/POLYM12040769",
            "score": 0.69,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Leno Mascia, Yannis Kouparitsas, Davide Nocita, Xujin Bao",
            "abstract": "Antiplasticization of glassy polymers, arising from the addition of small amounts of plasticizer, was examined to highlight the developments that have taken place over the last few decades, aiming to fill gaps of knowledge in the large number of disjointed publications. The analysis includes the role of polymer/plasticizer molecular interactions and the conditions leading to the cross-over from antiplasticization to plasticization. This was based on molecular dynamics considerations of thermal transitions and related relaxation spectra, alongside the deviation of free volumes from the additivity rule. Useful insights were gained from an analysis of data on molecular glasses, including the implications of the glass fragility concept. The effects of molecular packing resulting from antiplasticization are also discussed in the context of physical ageing. These include considerations on the effects on mechanical properties and diffusion-controlled behaviour. Some peculiar features of antiplasticization regarding changes in Tg were probed and the effects of water were examined, both as a single component and in combination with other plasticizers to illustrate the role of intermolecular forces. The analysis has also brought to light the shortcomings of existing theories for disregarding the dual cross-over from antiplasticization to plasticization with respect to modulus variation with temperature and for not addressing failure related properties, such as yielding, crazing and fracture toughness."
        },
        {
            "source": "scopus",
            "id": "85071027353",
            "title": "Cooperativity Scaling and Free Volume in Plasticized Polylactide",
            "date": "2019-08-27",
            "url": "https://doi.org/10.1021/acs.macromol.9b00464",
            "score": 0.6736,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Steven Araujo, Nicolas Delpouve, Sandra Domenek, Alain Guinault, Roman Golovchak, Roman Szatanik, Adam Ingram, Cyrille Fauchard, Laurent Delbreilh, Eric Dargent",
            "abstract": "The experimental evidence of the increase of activation energy associated with the super Arrhenius behavior governing amorphous polylactide by free volume variations has been obtained through a combination of calorimetric, dielectric, and positron annihilation lifetime measurements. The amount of free volume in polylactide was controlled by the amount of acetyltributylcitrate plasticizer in the composition. Plasticization is shown to decrease both the fragility index and the scale of cooperative motions at the glass transition. The calculations of volume and energetic components of kinetic fragility reveal that the fragility drop is governed by the change in the size of cooperative rearranging region. As a result, direct correlation has been established between cooperativity and activation energy for the entire plasticized polylactide series. It is also shown that cooperativity variations with both temperature and plasticizer content can be simplified as a master curve with free volume."
        },
        {
            "source": "scopus",
            "id": "85133551319",
            "title": "Segmental Relaxation Dynamics in Amorphous Polylactide Exposed to UV Light",
            "date": "2022-08-01",
            "url": "https://doi.org/10.1002/macp.202200085",
            "score": 0.6662,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Steven Araujo, Chlo\u00e9 Sainlaud, Nicolas Delpouve, Emmanuel Richaud, Laurent Delbreilh, Eric Dargent",
            "abstract": "The degradation of polylactide (PLA) under UV exposure is investigated in terms of cooperativity and kinetic fragility at the glass transition. In the first part, possibly coexisting degradation mechanisms are evoked from the interpretation of the infrared spectroscopy analyses. Furthermore, the reduction of PLA chain length, owing to photolytic scissions predominant over local crosslinks, is assessed from chromatography, and confirmed by the shift of the glass transition temperature toward lower temperature. Modulated temperature thermogravimetric analysis (MT-TGA) also shows that the activation energy needed to initiate thermal degradation falls after UV exposure. In the second part, the impact of UV-induced degradation on the cooperative rearranging region (CRR) size and the kinetic fragility, respectively, calculated thanks to calorimetric and dielectric measurements, is discussed. Despite the assumed concomitance of several degradation mechanisms, it is observed that the glass transition, the kinetic fragility, and the CRR size decrease together with the exposure time. Moreover, it is found that the data align well on another trend depicting the change in the relaxation properties caused by plasticization of PLA. Thus, the variations of segmental relaxation properties caused by UV may be related to the increase of free volume linked to the damaging of the PLA structure."
        },
        {
            "source": "scopus",
            "id": "85178091542",
            "title": "How temperature-induced depolymerization and plasticization affect the process of structural relaxation",
            "date": "2024-01-05",
            "url": "https://doi.org/10.1016/j.polymer.2023.126549",
            "score": 0.6642,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Roman Svoboda, Jana Machotov\u00e1, \u0160t\u011bp\u00e1n Podzimek, Pavla Honcov\u00e1, Maria Chrom\u010d\u00edkov\u00e1, Martina Nalezinkov\u00e1, Jan Loskot, Ale\u0161 Bezrouk, Daniel Jezbera",
            "abstract": "The self-plasticization, i.e., the increase in the polymer segmental mobility by the inclusion of its own monomer, has a major impact on the structural, thermal, and mechanical properties of the polymer. Differential scanning calorimetry (DSC) was used to investigate the influence of thermally induced self-plasticization on the structural relaxation of polydioxanone (PDX). Depolymerization (based dominantly on the end-chain scission mechanism) was found to be controlled by the depolymerization temperature Td as well as the actual number of re-melting cycles (while keeping the time spent at Td constant). PDX samples with the glass transition temperature (Tg) ranging from \u221252 (highly plasticized) to \u221213 \u00b0C (virgin) were prepared. The DSC data were described in terms of the Tool-Narayanaswamy model; a consistent structural relaxation behavior associating the degree of plasticization with Tg was identified. The activation energy first decreased with plasticization from 430 kJ mol\u22121 to 210 kJ mol\u22121 in the Tg range of \u221240 to \u221213C, which is consistent with the plasticization-caused spacing-apart of the polymer chains resulting in larger free volume and increased freedom for the relaxation movements. For the highly plasticized PDX samples, the activation energy increased from 210 kJ mol\u22121 to 310 kJ mol\u22121, which appears to be associated with the possible segregation of the portion of the plasticizer into a discrete phase. The width of the relaxation times distribution increased with plasticization as a consequence of the plasticizer loosening the polymeric chains and enabling a wider variety of the segmental movement. The plasticization also leads to a higher dependence of the segmental relaxation movements on their current physico-chemical and steric surrounding."
        },
        {
            "source": "scopus",
            "id": "85078349470",
            "title": "A simple mean-field model of glassy dynamics and glass transition",
            "date": "2020-01-01",
            "url": "https://doi.org/10.1039/c9sm01575b",
            "score": 0.6317,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Valeriy V. Ginzburg",
            "abstract": "We propose a phenomenological model to describe the equilibrium dynamic behavior of amorphous glassy materials. It is assumed that a material can be represented by a lattice of cooperatively re-arranging regions (CRRs), with each CRR having two states, the low-temperature \"solid\" and the high-temperature \"liquid\". At low temperatures, the material exhibits two characteristic relaxation times, corresponding to the slow large-scale motion between the \"solid\" CRRs (\u03b1-relaxation) and the faster local motion within individual CRRs (\u03b2-relaxation). At high temperatures, the \u03b1- and \u03b2-relaxation times merge, as observed experimentally and suggested by the \"Coupling Model\" framework. Our new approach is labeled \"Two-state, two (time)scale model\" or TS2. It is shown that the TS2 treatment can successfully describe the \"two-Arrhenius\" relaxation time behavior described in several recent experiments. We also apply TS2 to describe the pressure- and molecular-weight dependence of the glass transition temperature in bulk polymers, as well as its dependence on film thickness in thin films."
        },
        {
            "source": "scopus",
            "id": "85068762283",
            "title": "Dielectric and calorimetric signatures of chain orientation in strong and tough ultrafine electrospun polyacrylonitrile",
            "date": "2019-09-12",
            "url": "https://doi.org/10.1016/j.polymer.2019.121638",
            "score": 0.6165,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Steven Araujo, Nicolas Delpouve, Laurent Delbreilh, Dimitry Papkov, Dzenis, Eric Dargent",
            "abstract": "Ultrafine diameter fibers of polyacrylonitrile (PAN), obtained from electrospinning, have huge potential for structural applications since they exhibit an unusual combination of strength and toughness. However, the difficulty to characterize their supramolecular architecture limits their production at the industrial scale. In this work, the glass transition of electrospun nanofiber mats of PAN was investigated by means of thermal analysis techniques. Modulated temperature differential scanning calorimetry (MT\u2013DSC) and dielectric relaxation spectroscopy (DRS) were used, and relaxation parameters characteristic of the glass transition were obtained. Reduction in average fiber diameter resulted in broadening of the glass transition and a shift of its midpoint to higher temperatures as observed by MT\u2013DSC, revealing additional level of constraints in the amorphous phase. The DRS curves, obtained above the calorimetric signature of the glass transition, superimpose independently on the fiber diameter. This result, which contrasts with MT\u2013DSC observations, shows that the constraint of mobility evidenced at the glass transition, is suppressed when driving the fiber mat to higher temperatures. The dielectric strength increases with temperature, revealing an increase in the density of dipoles participating to the relaxation dynamics. This result, commonly attributed to the progressive mobilization of initially constrained amorphous phase, supports the hypothesis that electrospinning process induces higher level of polymer chain orientation at small fiber diameters, which fades away when crossing the glass transition. The orientation impacts the temperature dependence of the relaxation time close to the glass transition, as it shows higher deviation from Arrhenius behavior with the decrease of the fiber diameter. This leads to an increase of the fragility index which comes in opposition to the decrease in the cooperativity length, estimated from the temperature fluctuation approach of the cooperative rearranging region (CRR) concept. To explain this result, both volume and thermal contributions of the fragility index have been calculated, and a strong increase in the thermal contribution has been observed for the most oriented material. This result is interpreted as a signature of an increase in the polymer chain rigidity."
        },
        {
            "source": "eric",
            "id": "EJ348017",
            "title": "Introducing Plastics in the Laboratory: Synthesis of a Plasticizer, Dioctylphthalate and Evaluation of its Effects on the Physical Properties of Polystyrenes.",
            "date": "1986",
            "url": "https://eric.ed.gov/?id=EJ348017",
            "score": 0.591,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Caspar, A., And Others",
            "abstract": "Proposes a two-stage experimental approach that combines preparative chemistry and polymer characterization. Describes the simple organic synthesis of a plasticizer, the dioctylphthalate, and its direct use in the preparation of a styrene/divinylbenzene network copolymer. Discusses how to evaluate the physical properties of the resulting plastic. (TW)\n\nType: Journal Articles, Guides - Classroom - Teacher | Language: English | Peer Reviewed"
        },
        {
            "source": "scopus",
            "id": "85097139614",
            "title": "Molecular mobility in amorphous biobased copolyesters obtained with 2,5- and 2,4-furandicarboxylate acid",
            "date": "2021-01-20",
            "url": "https://doi.org/10.1016/j.polymer.2020.123225",
            "score": 0.5899,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Aur\u00e9lie Bourdet, Steven Araujo, Shanmugam Thiyagarajan, Laurent Delbreilh, Antonella Esposito, Eric Dargent",
            "abstract": "Poly(ethylene 2,5-furandicarboxylate) (2,5-PEF) is one of the most credible biobased alternative to poly (ethylene terephthalate) (PET). The Henkel disproportionation reaction that leads to furandicarboxylic acid (FDCA) provides three position isomers: 2,5-FDCA (obtained with the highest yield), 2,4-FDCA (so far considered as a by-product), and 3,4-FDCA (traces). The copolymerization of the two main isomers of FDCA with a diol, e.g. ethylene glycol (EG), is an interesting approach to obtain a family of furan-based biopolymers with adjusted physical properties. This work investigates the molecular mobility of three copolymers obtained with EG and ratios of 2,5-FDCA and 2,4-FDCA ensuring the complete disruption of crystallization (90:10, 85:15 and 50:50 mol % of 2,5:2,4 FDCA), as compared to the homopolymers 2,5-PEF and 2,4-PEF. The molecular mobility was investigated by cross-comparing the results obtained by Modulated-Temperature Differential Scanning Calorimetry (MT-DSC), Dielectric Relaxation Spectroscopy (DRS) and Thermo-Stimulated Depolarization Currents (TSDC), with the aim of evaluating the local and segmental molecular mobilities, their activation energies, as well as the temperature dependence of the relaxation time and of the cooperatively rearranging regions at the glass transition. The furan ring in 2,5-FDCA (2,5-PEF) has a rotation axis that is less linear compared to the benzene ring in terephthalic acid (PET), with consequences on the ring-flipping mechanisms. 2,5-FDCA and 2,4-FDCA differ by the position of the carbonyl groups on the furan ring, which adds asymmetry to non-linearity. The incorporation of 2,4-FDCA-based units into a polymer backbone mainly constituted of 2,5-FDCA-based repeating units is responsible for longer relaxation times associated with the local \u03b2 relaxation processes, no striking effects on the kinetic fragility index m, no obvious effects on cooperativity (a slightly increase in the cooperativity length is observed in the liquid state), no effects on the activation energy for the segmental \u03b1 relaxation in the liquid state, and a decrease in the activation energy in the glassy state."
        },
        {
            "source": "scopus",
            "id": "85082765328",
            "title": "Distinct dynamics of structural relaxation in the amorphous phase of poly(l-lactic acid) revealed by quiescent crystallization",
            "date": "2020-04-07",
            "url": "https://doi.org/10.1039/c9sm02541c",
            "score": 0.5795,
            "cpc_sections": [],
            "cpc_groups": [],
            "by": "Xavier Monnier, Nicolas Delpouve, Allisson Saiter-Fourcin",
            "abstract": "Fast scanning calorimetry (FSC) experiments were performed to investigate physical aging in amorphous and semi-crystalline poly(l-lactic acid)s (PLLAs) that were thermally crystallized under conditions leading to the \u03b1\u2032- or \u03b1-crystalline form, and either favouring or inhibiting the development of a rigid amorphous fraction (RAF). The enthalpy of recovery was calculated after two procedures of rescaling to the content of the whole amorphous phase and also to the only content of the mobile amorphous fraction (MAF), which helped in clarifying the contribution of the RAF. From the dependence of the structural relaxation rate on the aging temperature, two regimes were evidenced for all samples. In the aging temperature domain situated close to the glass transition, the structural relaxation occurs significantly faster in the MAF. Its rate is independent of the aging temperature and is not influenced by the microstructure. However, the distance to equilibrium is higher in samples for which the coupling is strong between crystal and amorphous, implying that the time to reach equilibrium is also higher. In contrast, at low aging temperatures, for which the whole amorphous phase can be considered as solid, MAF and RAF exhibit the same structrural relaxation rate. This convergence in the relaxation kinetics by decreasing the temperature of physical aging was interpreted as the evolution of relaxation dynamics in the MAF from segmental to local. This change is highlighted by the comparison between MAF and RAF relaxation kinetics, but it occurs similarly in a pure amorphous system."
        }
    ],
    "top_references_patents": [
            {
                "source": "patentsview",
                "id": "10000049",
                "title": "Methods and apparatus for applying protective films",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000049",
                "score": 0.4561,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: EXEL INDUSTRIES, Inventor: Michael DeFillipi",
                "abstract": "An applicator die for creating and applying laminarized ribbons of polymeric film to a target surface, such as but not limited to a surface of an automobile body component. In one embodiment, the protective film is an aqueous emulsion of polyvinyl acetate and is used to create a continuous peelable film to protect a surface. In another embodiment, the polymeric is polyvinyl chloride and it is applied to create an anti-chip coating. The applicator die has an internal supply gallery and an outlet slot of complex shape to emit a laminarized ribbon of polymer-based material that allows the material to be applied directly to the target surface without masking. A robot is used to control movement of the die. The die includes temperature control."
            },
            {
                "source": "patentsview",
                "id": "10000048",
                "title": "Taping tool having improved tape advance",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000048",
                "score": 0.4493,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: GRACO INC., Assignee: AXIA ACQUISITION CORPORATION, Inventor: Jeromy D. Horning, Inventor: Matthew W. Jungklaus, Inventor: Steven J. Wrobel",
                "abstract": "A taping apparatus includes an elongate body portion having a moveable control member for controlling the advancement of tape and a head portion connected to the elongate body portion for advancing the tape. The head portion includes a first stop, a second stop, a guide extending from the first stop to the second stop, and a tape advance mechanism moveable along the guide. The tape advance mechanism and the control member are coupled to one another such that the tape advance mechanism is moveable in response to movement of the control member. The tape advance mechanism includes a rotatable cam and a needle that rotates with the cam."
            },
            {
                "source": "patentsview",
                "id": "10000002",
                "title": "Method for manufacturing polymer film and co-extruded film",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000002",
                "score": 0.4469,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: KOLON INDUSTRIES, INC., Inventor: Dong Jin Kim, Inventor: Si Min Kim, Inventor: Yun-Jo Kim, Inventor: Dong-Hyeon Choi",
                "abstract": "The present invention relates to: a method for manufacturing a polymer film, the method including a base film forming step for co-extruding a first resin containing a polyamide-based resin and a second resin containing a copolymer including polyamide-based segments and polyether-based segments; a co-extruded film including a base film including a first resin layer containing a polyamide-based resin, and a second resin layer containing a copolymer having polyamide-based segments and polyether-based segments; to a co-extruded film including a base film including a first resin layer and a second resin layer, which have different melting points; and to a method for manufacturing a polymer film, the method including a base film forming step including a step of co-extruding a first resin and a second resin, which have different melting points."
            },
            {
                "source": "patentsview",
                "id": "10000027",
                "title": "Apparatus and method for reshaping plastic preforms into plastic containers with an automatic changing device for handling parts",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000027",
                "score": 0.4459,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: KRONES AG, Inventor: Klaus Voth, Inventor: Wolfgang Schoenberger",
                "abstract": "A plant for reshaping plastic preforms into plastic containers, includes a heating device for heating the plastic preforms, and a device for reshaping the plastic preforms into the plastic containers, arranged downstream of the heating device in the transport direction of the plastic preforms, wherein the reshaping device includes a transport device, which transports the plastic preforms along a predefined transport path and wherein the transport device has a station carrier on which a multitude of reshaping stations are arranged, each having blow mold devices each arranged on blow mold carriers. The reshaping device includes a changing device, which is suited and intended for at least removing and/or attaching the blow mold devices to the blow mold carriers, wherein this changing device is further suited and intended for at least removing and/or attaching the changeable element to the heating device."
            },
            {
                "source": "patentsview",
                "id": "10000028",
                "title": "Mechanical fastening nets and methods of making the same",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000028",
                "score": 0.4408,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: 3M INNOVATIVE PROPERTIES COMPANY, Inventor: Ronald W. Ausen, Inventor: Thomas P. Hanschen, Inventor: William J. Kopecky, Inventor: William C. Unruh",
                "abstract": "A method of making a mechanical fastening net. The method includes providing a net having strands of polymer and open areas between the strands of polymer and molding a portion of the polymer in the strands of the net into upstanding posts to form the mechanical fastening net. A mechanical fastening net that includes a polymeric backing, a plurality of openings in the polymeric backing, and upstanding posts on at least one of the first or second major surface of the polymeric backing is also disclosed. The polymeric backing has a range of thicknesses ranging from minimum to maximum thickness, and for at least a portion of the polymeric backing, the minimum thickness of the polymeric backing is where it abuts one of the openings."
            },
            {
                "source": "patentsview",
                "id": "10000043",
                "title": "Multilayer film for resealable packaging having improved resealing",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000043",
                "score": 0.4365,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: BOSTIK SA, Inventor: Christophe Robert, Inventor: Ludovic Sallet, Inventor: Christophe Notteau",
                "abstract": "Multilayer film comprising two thin layers D and E of a thermoplastic material bonded to one another by a continuous layer A that is a hot-melt pressure-sensitive adhesive composition:"
            },
            {
                "source": "patentsview",
                "id": "10000042",
                "title": "Tearable polystyrene film laminate for packaging and pouch purposes",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000042",
                "score": 0.429,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: Multi-Plastics, Inc., Inventor: M. David Parsio",
                "abstract": "The current disclosure relates to a polymeric laminate structure having an outer polystyrene film, either blown or cast, comprised of crystal polystyrene homopolymer, optionally blended with up to about 45 wt-% of high impact polystyrene and/or inorganic fillers."
            },
            {
                "source": "patentsview",
                "id": "10000047",
                "title": "Method for manufacturing curved liquid crystal display panel",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000047",
                "score": 0.42,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: WUHAN CHINA STAR OPTOELECTRONICS TECHNOLOGY CO., LTD., Inventor: Dandan Liu, Inventor: Tsungying Yang, Inventor: Haiyan Sun, Inventor: Dejiun Li",
                "abstract": "The present invention provides a method for manufacturing a curved liquid crystal display panel, which comprises coating a sealing gum on a first or a second frame sealing region; filing liquid crystals between the two substrates and adhering the two substrates together; performing a first curing on partial sealing gum on a first set or a third set of frame bodies; bending the first set and the third set of frame bodies obtained after the first curing along the extension direction of the first set of frame bodies; performing a second curing on uncured sealing gum on the two bended substrates."
            },
            {
                "source": "patentsview",
                "id": "10000004",
                "title": "Process of obtaining a double-oriented film, co-extruded, and of low thickness made by a three bubble process that at the time of being thermoformed provides a uniform thickness in the produced tray",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000004",
                "score": 0.4095,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: ZUBEX INDUSTRIAL SA DE CV, Inventor: Miguel Jorge Zubiria Elizondo, Inventor: Jose Juan Valadez Lopez",
                "abstract": "The present invention relates to provides a double-oriented film, co-extrude, and of low thickness, with a layered composition that gives the property of being of high barrier to gases and manufactured by the process of co-extrusion of 3 bubbles, which gives the property of when being thermoformed, ensure the distribution of uniform thickness in the walls, base, folds, and corners of the formed tray saving a minimum of 50% of plastic without diminishing its gas barrier and its resistance to puncture."
            },
            {
                "source": "patentsview",
                "id": "10000015",
                "title": "Methods for making optical components, optical components, and products including same",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000015",
                "score": 0.3985,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: SAMSUNG ELECTRONICS CO., LTD., Inventor: Robert J. Nick",
                "abstract": "A hermetically sealed optical component includes an optical material including an optical material comprising quantum dots sealed between glass substrates by a hermetic seal including a liquid crystalline polymer."
            },
            {
                "source": "patentsview",
                "id": "10000011",
                "title": "Supports for sintering additively manufactured parts",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000011",
                "score": 0.3928,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: MARKFORGED, INC, Inventor: Gregory Thomas Mark",
                "abstract": "To reduce distortion in an additively manufactured part, a shrinking platform is formed from a metal particulate filler in a debindable matrix. Shrinking supports of the same material are formed above the shrinking platform, and a desired part of the same material is formed upon them. A sliding release layer is provided below the shrinking platform of equal or larger surface area than a bottom of the shrinking platform to lateral resistance between the shrinking platform and an underlying surface. The matrix is debound sufficient to form a shape-retaining brown part assembly including the shrinking platform, shrinking supports, and the desired part. The shape-retaining brown part assembly is heated to shrink all of the components together at a same rate via atomic diffusion."
            },
            {
                "source": "patentsview",
                "id": "10000014",
                "title": "Method for producing thermoplastic foam panels by means of at least two heating elements offset in parallel with each other",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000014",
                "score": 0.3888,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: BASF SE, Inventor: Dietrich Scherzer, Inventor: Tim DIEHLMANN, Inventor: Carsten SANDNER, Inventor: Franz-Josef Dietzen, Inventor: Herbert Schall",
                "abstract": "The present invention relates to a process for the production of at least two-layer thermoplastic foam sheets via thermal welding of at least two thinner thermoplastic foam sheets. In the process of the invention, at least two heating elements are conducted on mutually offset planes between the surfaces to be welded of the thinner thermoplastic foam sheets, and the foam sheets here do not touch the heating elements. The number of layers of the thermoplastic foam sheet is per se a result of the number of thinner thermoplastic foam sheets that are thermally welded to one another. If by way of example three thinner thermoplastic foam sheets are thermally welded to one another, a three-layer thermoplastic foam sheet is per se obtained, and if there are four thinner thermoplastic foam sheets the result is accordingly per se a four-layer thermoplastic foam sheet."
            },
            {
                "source": "patentsview",
                "id": "10000025",
                "title": "Optimized cross-ply orientation in composite laminates",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000025",
                "score": 0.3873,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: The Boeing Company, Inventor: Max U. Kismarton",
                "abstract": "A composite laminate has a primary axis of loading and comprises a plurality resin plies each reinforced with unidirectional fibers. The laminate includes cross-plies with fiber orientations optimized to resist bending and torsional loads along the primary axis of loading."
            },
            {
                "source": "patentsview",
                "id": "10000009",
                "title": "Sterile environment for additive manufacturing",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000009",
                "score": 0.3744,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Inventor: Nathan Christopher Maier",
                "abstract": "In sterile, additive manufacturing wherein one lamella is successively built upon an underlying lamella until an object is completed, a sterile manufacturing environment is provided. A major chamber large enough to accommodate the manufactured object has sterile accordion pleated sidewalls and a sterile top closed with flap valves. A minor chamber for supporting the nozzles positioned above the major chamber has similar valves in corresponding positions. Nozzles for material deposition penetrate the pair of valves to block air and particles from entry into the major chamber where the nozzles make layer by layer deposition of the object using XY areawise nozzle motion relative to the object as well as Z nozzle vertical motion with the major chamber expanding as the object is formed."
            },
            {
                "source": "patentsview",
                "id": "10000037",
                "title": "Transparent laminate and protective tool including the same",
                "date": "2018-06-19",
                "url": "https://patents.google.com/patent/US10000037",
                "score": 0.3678,
                "cpc_sections": [],
                "cpc_groups": [],
                "by": "Assignee: DEXERIALS CORPORATION, Inventor: Emi Yoshida, Inventor: Eiji Ohta, Inventor: Kimitaka Nishimura, Inventor: Shinichi Matsumura, Inventor: Shigehisa Ohkawara",
                "abstract": "The purpose of the present invention is to prevent an increase in reflectance and a decrease in transmittance, retain the intact instantaneousness and ease of stripping, improve the releasability of the adhesive, avoid the generation of distortion due to the thickness of the adhesive, and ensure the visibility, by laminating filmy members (10) each equipped with a moth-eye structure (12). This transparent laminate (1) comprises a plurality of filmy members (10) which each comprise a base (11) and, disposed on at least one surface thereof, a structure (12) made up of recesses and protrusions which have been regularly arranged at a pitch not longer than the wavelengths of visible light. At least the ends of the filmy members (10) have been superposed, with a pressure-sensitive adhesive layer (2) interposed therebetween. In the superposed filmy members (10), there is a space (14) between the opposed structures (12)."
            }
        ],
}

def get_id_inserted(conn):
    stmt_id = ibm_db.exec_immediate(conn, "VALUES IDENTITY_VAL_LOCAL()")
    row = ibm_db.fetch_tuple(stmt_id)
    return row[0] if row else None

def clean_for_json(obj):
    """Limpia recursivamente objetos para JSON compatible con DB2"""
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, str):
        # Eliminar caracteres problemáticos
        cleaned = obj.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        # Eliminar caracteres de control excepto \n, \r, \t
        cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char in '\n\r\t')
        return cleaned
    else:
        return obj

def safe_json_dumps(data):
    """Convierte datos a JSON seguro para DB2 CLOB"""
    if not data:
        return ""
    try:
        cleaned_data = clean_for_json(data)
        return json.dumps(cleaned_data, ensure_ascii=False, separators=(',', ':'))
    except Exception as e:
        print(f"Error al serializar JSON: {e}")
        return "{}" if isinstance(data, dict) else "[]"

# Preparar los datos JSON
top_references_json = safe_json_dumps(report.get("top_references", []))
top_patents_json = safe_json_dumps(report.get("top_references_patents", []))
top_articles_json = safe_json_dumps(report.get("top_references_articles", []))

# Debug: verificar longitud de los strings
print(f"Longitud top_references_json: {len(top_references_json)}")
print(f"Longitud top_patents_json: {len(top_patents_json)}")
print(f"Longitud top_articles_json: {len(top_articles_json)}")

id_parametros = 28  # Ejemplo de ID de parámetros
id_modulos = 21     # Ejemplo de ID de módulos
query_respuesta = f"""
INSERT INTO SOTRI.T_OTRI_PI_RESPUESTA (
    IDOTRIPIPROCESO, IDOTRIPIPARAMETROS, IDOTRIPIMODULOS, MARCATIEMPOISO,
    REFERENCPRINCIPALES, REFERENCIASPATENTES, REFERENCIAARTICULOS
) VALUES (
    {id_proceso}, {id_parametros}, {id_modulos}, 
    '{report.get("timestamp", "")}',
    '{top_references_json.replace("'", "''")}',
    '{top_patents_json.replace("'", "''")}',
    '{top_articles_json.replace("'", "''")}'
)
"""

ibm_db.exec_immediate(conn, query_respuesta)
id_respuesta = get_id_inserted(conn)
print(f"ID Respuesta insertado: {id_respuesta}")

ibm_db.close(conn)

print("Registro consultado correctamente")

