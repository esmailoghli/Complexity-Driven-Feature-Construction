#\addplot+[mark=triangle*] coordinates{(4,0.149835526316)};

mappnames = {1:'TPE(Variance)',
			 2: 'TPE($\chi^2$))',
			 3:'TPE(FCBF))',
			 4: 'TPE(Fisher Score))',
			 5: 'TPE(Mutual Information))',
			 6: 'TPE(MCFS))',
			 7: 'TPE(ReliefF))',
			 8: 'TPE(no ranking)',
             9: 'Simulated Annealing(no ranking)',
			 10: 'NSGA-II(no ranking)',
			 11: 'Exhaustive Search(no ranking)',
			 12: 'Forward Selection(no ranking)',
			 13: 'Backward Selection(no ranking)',
			 14: 'Forward Floating Selection(no ranking)',
			 15: 'Backward Floating Selection(no ranking)',
			 16: 'RFE(Logistic Regression)'
			 }

experiment_data = {(200, 1, 'ranking_avg'): 0.00021767616271972656, (200, 1, 'ranking_std'): 0.0002275988761973168, (200, 1, 'selection_avg'): 0.00611790960485285, (200, 1, 'selection_std'): 0.0029900719016180298, (200, 2, 'ranking_avg'): 0.0013483285903930664, (200, 2, 'ranking_std'): 0.000263706276027355, (200, 2, 'selection_avg'): 0.006608260761607777, (200, 2, 'selection_std'): 0.0028147156886308205, (200, 3, 'ranking_avg'): 0.016391587257385255, (200, 3, 'ranking_std'): 0.007510686030456249, (200, 3, 'selection_avg'): 0.006498000838539817, (200, 3, 'selection_std'): 0.0030602836849558048, (200, 4, 'ranking_avg'): 0.010993719100952148, (200, 4, 'ranking_std'): 0.00327086180689552, (200, 4, 'selection_avg'): 0.00865421945398504, (200, 4, 'selection_std'): 0.005960158347371066, (200, 5, 'ranking_avg'): 0.12404487133026124, (200, 5, 'ranking_std'): 0.09028223227103982, (200, 5, 'selection_avg'): 0.007179862802678888, (200, 5, 'selection_std'): 0.005245667272981065, (200, 6, 'ranking_avg'): 0.05289900302886963, (200, 6, 'ranking_std'): 0.016032139721329344, (200, 6, 'selection_avg'): 0.006874910267916592, (200, 6, 'selection_std'): 0.004079695539359497, (200, 7, 'ranking_avg'): 0.2811717987060547, (200, 7, 'ranking_std'): 0.02660421834174795, (200, 7, 'selection_avg'): 0.008060372959483754, (200, 7, 'selection_std'): 0.012605025658420458, (1000, 1, 'ranking_avg'): 0.0001708984375, (1000, 1, 'ranking_std'): 3.427971684546396e-05, (1000, 1, 'selection_avg'): 0.007688253576105291, (1000, 1, 'selection_std'): 0.0046165189705656235, (1000, 2, 'ranking_avg'): 0.0012702703475952148, (1000, 2, 'ranking_std'): 0.0002197160240736479, (1000, 2, 'selection_avg'): 0.007286585461009632, (1000, 2, 'selection_std'): 0.005129128641295824, (1000, 3, 'ranking_avg'): 0.03583073616027832, (1000, 3, 'ranking_std'): 0.014194612574913092, (1000, 3, 'selection_avg'): 0.00830224860798229, (1000, 3, 'selection_std'): 0.00619435055663142, (1000, 4, 'ranking_avg'): 0.1481790542602539, (1000, 4, 'ranking_std'): 0.03262610862198616, (1000, 4, 'selection_avg'): 0.0072737281972711735, (1000, 4, 'selection_std'): 0.004783653571397829, (1000, 5, 'ranking_avg'): 0.19385924339294433, (1000, 5, 'ranking_std'): 0.0213425417286743, (1000, 5, 'selection_avg'): 0.006644355167042125, (1000, 5, 'selection_std'): 0.004950982071477797, (1000, 6, 'ranking_avg'): 0.2020923137664795, (1000, 6, 'ranking_std'): 0.0665282109687488, (1000, 6, 'selection_avg'): 0.007593083381652832, (1000, 6, 'selection_std'): 0.004171743385276964, (1000, 7, 'ranking_avg'): 2.2240671873092652, (1000, 7, 'ranking_std'): 0.4420683535108195, (1000, 7, 'selection_avg'): 0.009538509628989479, (1000, 7, 'selection_std'): 0.006736907517648705, (2000, 1, 'ranking_avg'): 0.00021483898162841797, (2000, 1, 'ranking_std'): 3.767367388609277e-05, (2000, 1, 'selection_avg'): 0.007863103259693492, (2000, 1, 'selection_std'): 0.00573904885398177, (2000, 2, 'ranking_avg'): 0.0019596338272094725, (2000, 2, 'ranking_std'): 0.001353038939227984, (2000, 2, 'selection_avg'): 0.00821286765011874, (2000, 2, 'selection_std'): 0.009177307960536627, (2000, 3, 'ranking_avg'): 0.04769573211669922, (2000, 3, 'ranking_std'): 0.010439772927644373, (2000, 3, 'selection_avg'): 0.007681580023332075, (2000, 3, 'selection_std'): 0.005971719484121589, (2000, 4, 'ranking_avg'): 0.6702346324920654, (2000, 4, 'ranking_std'): 0.16058722191207228, (2000, 4, 'selection_avg'): 0.007100020755421032, (2000, 4, 'selection_std'): 0.004113513029402159, (2000, 5, 'ranking_avg'): 0.3271944999694824, (2000, 5, 'ranking_std'): 0.05989689369220183, (2000, 5, 'selection_avg'): 0.008512988957491788, (2000, 5, 'selection_std'): 0.005318021001050209, (2000, 6, 'ranking_avg'): 0.8741105079650879, (2000, 6, 'ranking_std'): 0.13063516853388993, (2000, 6, 'selection_avg'): 0.007292025739496405, (2000, 6, 'selection_std'): 0.00390706894217376, (2000, 7, 'ranking_avg'): 4.402861189842224, (2000, 7, 'ranking_std'): 0.2362210791478189, (2000, 7, 'selection_avg'): 0.00707749453457919, (2000, 7, 'selection_std'): 0.0043313163138476414, (20000, 1, 'ranking_avg'): 0.0008242607116699218, (20000, 1, 'ranking_std'): 0.00010431589642618356, (20000, 1, 'selection_avg'): 0.009066932851617986, (20000, 1, 'selection_std'): 0.006762222015541567, (20000, 2, 'ranking_avg'): 0.006072521209716797, (20000, 2, 'ranking_std'): 0.0027751157383839485, (20000, 2, 'selection_avg'): 0.010235170884565874, (20000, 2, 'selection_std'): 0.00719038004739668, (20000, 3, 'ranking_avg'): 0.617911410331726, (20000, 3, 'ranking_std'): 0.11511321619324712, (20000, 3, 'selection_avg'): 0.012063993107188831, (20000, 3, 'selection_std'): 0.010294364540920002, (20000, 4, 'ranking_avg'): 74.60244596004486, (20000, 4, 'ranking_std'): 5.718245739939558, (20000, 4, 'selection_avg'): 0.009832653132351961, (20000, 4, 'selection_std'): 0.006498808073814724, (20000, 5, 'ranking_avg'): 3.740761733055115, (20000, 5, 'ranking_std'): 0.8035481480785808, (20000, 5, 'selection_avg'): 0.010125832124189897, (20000, 5, 'selection_std'): 0.009123933096913058, (20000, 6, 'ranking_avg'): 512.8771488904953, (20000, 6, 'ranking_std'): 33.84306825791305, (20000, 6, 'selection_avg'): 0.009024234251542525, (20000, 6, 'selection_std'): 0.005978381152320913, (20000, 7, 'ranking_avg'): 223.72367331981658, (20000, 7, 'ranking_std'): 8.829474121983559, (20000, 7, 'selection_avg'): 0.008513368259776723, (20000, 7, 'selection_std'): 0.004929062199622206, (200000, 1, 'ranking_avg'): 0.01267096996307373, (200000, 1, 'ranking_std'): 0.005056797009290162, (200000, 1, 'selection_avg'): 0.010316205024719239, (200000, 1, 'selection_std'): 0.008658483283175663, (200000, 2, 'ranking_avg'): 0.055594372749328616, (200000, 2, 'ranking_std'): 0.03843749162979099, (200000, 2, 'selection_avg'): 0.009832421216097745, (200000, 2, 'selection_std'): 0.006219520739646903, (200000, 3, 'ranking_avg'): 4.91871395111084, (200000, 3, 'ranking_std'): 0.5864616079636265, (200000, 3, 'selection_avg'): 0.009650457989085804, (200000, 3, 'selection_std'): 0.005860268094661107}

latex_string = ""
for s in range(1, 8):
	latex_string += "\\addplot+[mark=triangle*] coordinates{"
	for number_observations in [200, 1000,2000,20000]:
		#latex_string += "(" + str(number_observations) + ", " + str(experiment_data[(number_observations, s, 'selection_avg')]) + ') '
		latex_string += "(" + str(int(number_observations / 2.0)) + ", " + str(
			experiment_data[(number_observations, s, 'ranking_avg')]) + ') '
	latex_string += "};\n"
	latex_string += "\\addlegendentry{" + mappnames[s] + "}\n\n"

print(latex_string)