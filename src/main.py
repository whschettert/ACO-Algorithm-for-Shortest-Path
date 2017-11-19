import graph as graph
import time
import pickle
from aco import *
import parallel_aco as paco
import shortest_aco as short_aco

class Main:

    def __init__(self):
        gp = graph.Graph()

        # start_time = time.time()

        gp.build_graph_stop_points(250)

        # elapsed_time = time.time() - start_time

        # print "Time build graph %.2f seconds." % elapsed_time

        # print "Nodes: %d Edges: %d" % (gp.graph.number_of_nodes(), gp.graph.number_of_edges())

        # ALFA se 0 somente heuristica importa
        # BETA se 0 somente info feromonio importa

        # while True:
            # input = raw_input('Nodos(origem,destino) >>')
            # args = input.split(',')
        # args = ['1S0','8S37']

        nodes = [
                ['323S1','551S16'],
                ['375S8','452S3'],
                ['363S15','583S6'],
                ['315S11','245S12'],
                ['98S8','591S63'],
                ['559S13','540S3'],
                ['357S3','287S12'],
                ['470S7','637S25'],
                ['615S2','637S28'],
                ['465S12','637S26']]


        # print gp.compute_path(['1S0', '1S1', '1S2', '415S10', '415S11', '1S3', '1S4', '1S5', '1S6', '1S7', '1S8', '1S9', '288S12', '8S15', '8S16', '8S18', '8S19', '8S20', '8S21', '8S22', '8S23', '8S24', '8S25', '8S26', '8S27', '8S28', '8S29', '8S30', '8S31', '8S32', '418S2', '8S33', '8S34', '8S35', '8S36', '8S37'],'weight')

        start_time = time.time()
        for n in nodes:
            start_time = time.time()
            star_path, cost = gp.astar(n[0], n[1], 'travelTime')
            print 'A*: (custo, path):', cost, star_path, len(star_path), time.time() - start_time
            
            start_time = time.time()
            dij, cost = gp.dj(n[0], n[1], 'travelTime')
            print 'Dijkstra: (custo, path):', cost, dij, len(dij), time.time() - start_time

            print ''

        print '\n', len(['465S12','531S14','531S15','531S16','531S17','531S18','531S19','531S20','531S21','531S22','531S23','531S24','531S25','531S26','531S27','434S3','160S15','434S5','434S6','434S7','585S6','585S7','585S8','314S26','170S6','381S4','381S5','381S6','372S6','372S7','372S8','372S9','372S10','336S14','470S8','470S9','470S10','470S11','470S12','470S13','470S14','470S15','470S16','470S17','470S18','470S19','591S2','637S0','637S1','637S2','299S2','637S4','637S5','637S6','637S7','637S8','637S9','637S10','637S11','637S12','637S13','637S14','637S15','637S16','637S17','637S18','637S19','637S20','637S21','637S22','637S23','637S24','637S25','637S26'])
        print '\n', len( ['615S2','615S3','615S4','615S5','615S6','615S7','615S8','615S9','615S10','615S11','527S13','379S8','379S9','379S10','379S11','379S12','379S13','379S14','379S15','379S16','379S17','379S18','379S19','379S20','379S21','637S7','637S8','637S9','637S10','637S11','637S12','637S13','637S14','637S15','637S16','637S17','637S18','637S19','637S20','637S21','637S22','637S23','637S24','637S25','637S26','637S27','637S28'])
        print '\n', len( ['470S7','470S8','470S9','470S10','470S11','470S12','470S13','470S14','470S15','470S16','470S17','470S18','470S19','591S2','637S0','637S1','637S2','299S2','637S4','637S5','637S6','637S7','637S8','637S9','637S10','637S11','637S12','637S13','637S14','637S15','637S16','637S17','637S18','637S19','637S20','637S21','637S22','637S23','637S24','637S25'])
        print '\n', len( ['357S3','357S4','357S5','357S6','357S7','357S8','357S9','357S10','357S11','357S12','357S13','357S14','409S9','409S10','409S11','409S12','409S13','228S0','285S0','285S1','31S20','285S3','285S4','114S5','605S3','605S4','605S5','605S6','605S7','605S8','605S9','605S10','414S14','414S15','414S16','414S17','414S18','414S19','414S20','414S21','414S22','414S23','414S24','414S25','414S26','414S27','414S28','414S29','414S30','457S1','457S2','457S3','457S4','457S5','457S6','457S7','457S8','457S9','457S10','464S10','464S11','372S1','378S0','378S1','378S2','378S3','378S4','378S5','378S6','378S7','378S8','131S6','323S4','588S13','588S14','588S15','537S2','537S3','553S20','553S21','553S22','537S8','537S9','537S10','310S0','537S12','537S13','537S14','537S15','537S16','537S17','537S18','497S0','497S1','497S2','497S3','497S4','504S10','139S11','108S4','360S5','360S6','302S3','360S8','360S9','363S10','363S11','363S12','363S13','363S14','363S15','363S16','363S17','363S18','363S19','559S21','559S22','559S23','559S24','559S25','559S26','287S6','287S7','287S8','287S9','287S10','287S11','287S12'])
        #print '\n', len(['629S1','252S14','12S12','463S1','463S2','491S6','555S11','555S12','555S13','555S14','555S15','555S16','555S17','461S9','461S10','461S11','296S6','461S13','461S14','393S3','393S4','393S5','393S6','303S5','303S6','303S7','303S8','303S9','303S10','303S11','591S0','591S1','591S2','591S3','591S4','350S1','591S6','591S7','591S8','347S4','591S10','591S11','591S12','591S13','591S14','591S15','591S16','149S12','591S18','591S19','591S20','591S21','591S22','591S23','591S24','591S25','591S26','591S27','591S28','591S29','591S30','591S31','591S32','591S33','591S34','591S35','591S36','591S37','591S38','591S39','591S40','591S41','591S42','591S43','42S34','591S45','591S46','591S47','591S48','42S31','591S50','591S51','575S1','575S2','575S3','575S4','575S5','575S6','575S7'])
        print '\n', len( ['98S8','473S16','465S11','531S14','531S15','531S16','531S17','531S18','531S19','531S20','531S21','531S22','531S23','531S24','531S25','531S26','531S27','434S3','160S15','434S5','434S6','434S7','585S6','585S7','585S8','314S26','170S6','381S4','381S5','381S6','372S6','372S7','372S8','372S9','372S10','336S14','470S8','470S9','470S10','470S11','470S12','470S13','470S14','470S15','470S16','470S17','470S18','470S19','591S2','591S3','436S5','271S5','147S8','436S8','436S9','591S61','591S62','591S63'])
        print '\n', len( ['315S11','315S12','454S6','17S8','454S8','454S9','454S10','454S11','454S12','454S13','454S14','414S24','414S25','414S26','414S27','414S28','414S29','414S30','457S1','457S2','457S3','457S4','457S5','457S6','457S7','457S8','457S9','457S10','464S10','464S11','372S1','378S0','378S1','378S2','378S3','378S4','378S5','378S6','378S7','378S8','131S6','323S4','588S13','588S14','588S15','537S2','537S3','553S20','553S21','553S22','537S8','537S9','537S10','310S0','537S12','537S13','537S14','537S15','537S16','537S17','537S18','497S0','497S1','497S2','497S3','497S4','504S10','139S11','108S4','360S5','360S6','302S3','302S4','447S7','318S7','318S8','318S9','318S10','318S11','318S12','245S12'])
        print '\n', len( ['363S15','363S16','363S17','363S18','363S19','559S21','559S22','559S23','559S24','559S25','559S26','559S27','559S28','559S29','559S30','559S31','559S32','200S2','559S34','496S3','496S4','496S5','496S6','496S7','496S8','496S9','496S10','496S11','327S2','327S3','327S4','403S9','403S10','403S11','528S12','528S13','528S14','528S15','528S16','528S17','528S18','528S19','528S20','528S21','528S22','459S2','528S24','528S25','528S26','528S27','583S2','583S3','583S4','583S5','583S6'])
        print '\n', len( ['375S8','375S9','442S0','513S9','513S10','513S11','513S12','647S2','454S3','454S4','454S5','454S6','17S8','454S8','454S9','454S10','454S11','454S12','454S13','454S14','454S15','454S16','454S17','454S18','454S19','454S20','454S21','454S22','12S3','599S1','599S2','599S3','599S4','599S5','599S6','143S2','463S4','76S4','606S5','606S6','606S7','606S8','606S9','491S1','491S2','491S3','491S4','491S5','491S6','491S7','270S0','452S1','452S2','452S3'])
        print '\n', len( ['323S1','323S2','131S6','323S4','588S13','588S14','588S15','537S2','537S3','553S20','553S21','553S22','537S8','537S9','537S10','310S0','537S12','537S13','537S14','537S15','537S16','537S17','537S18','497S0','497S1','497S2','559S32','200S2','559S34','496S3','496S4','496S5','496S6','496S7','496S8','496S9','496S10','496S11','496S12','496S13','303S5','303S6','303S7','303S8','303S9','303S10','303S11','591S0','591S1','591S2','591S3','591S4','350S1','591S6','591S7','366S2','366S3','366S4','366S5','366S6','366S7','366S8','416S16','416S17','611S10','611S11','611S12','110S2','611S14','611S15','611S16','611S17','69S8','226S18','449S21','449S22','449S23','449S24','226S24','551S16'])


        # for i in range(10):
        #     print 'Amostra %1d' % i
        #     start_time = time.time()
        #     aco = Aco(gp.graph, 0.0001, 1.2, 0, 0.5)
        #     aco_path, cost = aco.run(1000, args[0], args[1], 'weight')
        #     print 'ACO: (custo, path):', aco_path, cost, 'Run Time: ' + str(time.time()-start_time)
    

        # start_time = time.time()
        # p_aco = paco.Aco(gp.graph, 0.0001, 1.2, 0, 0.5)
        # aco_path, cost = p_aco.run(1000, args[0], args[1], 'weight')
        # print 'P_ACO: (custo, path):', aco_path, cost, 'Run Time: ' + str(time.time()-start_time)

        # Num Ants:1900 - Init pheromone:0.000161031217354 - Alpha:0.239075890865 - Beta:0 - Evaporation:0.647256741985

            # start_time = time.time()
            # s_aco = short_aco.Aco(gp.graph, 3000, 100, 0, 1.2, 0, 0.5, 'weight', args[0])
            # aco_path, cost = s_aco.run(args[1])
            # print 'SHORT_ACO: (custo, path):', cost, aco_path, 'Run Time: ' + str(time.time()-start_time)

        # gp.draw_graph(aco_path)

if __name__ == "__main__":
    Main()
    # try:
    #     main = Main()
    # except KeyboardInterrupt as k:
    #     pass
    # except Exception as e:
    #     raise e
    # finally:
    #     print '\nexiting'
