from config import get_config_arg



def get_valid_ingress_port():

        """get the existing ingress list from config.txt file
        """
        ingress_port = []
        ex_ingress_ports = []

        ingressPrtRange = (get_config_arg("cross_connects", "ingress_ports_range")).split('-')

        for i in range(int(ingressPrtRange[0]), int(ingressPrtRange[1])+1):
            ex_ingress_ports.append(i)


        final_ing_prt_list = []

        for i in range(0, 3):
            prt_num = ex_ingress_ports[i]
            ingress_port.append(prt_num)

        ing_str = str(ingress_port)
        for i in range(1, 8, 3):

            val = ''.join(ing_str[i])
            final_ing_prt_list.append(val)
            
        return final_ing_prt_list


def get_valid_egress_port():

    
        """get the existing egress port list from config.txt file
        """
        egress_port = []
        ex_egress_ports = []

        egressPrtRange = (get_config_arg("cross_connects", "egress_ports_range")).split('-')


        for j in range(int(egressPrtRange[0]), int(egressPrtRange[1])+1):
            ex_egress_ports.append(j)
      

        final_eg_prt_list = []

        for i in range(0, 3):
            prt_num = ex_egress_ports[i]
            egress_port.append(prt_num)

        eg_str = str(egress_port)
        for i in range(1, 10, 4):

            val = ''.join(eg_str[i])+''.join(eg_str[i+1])
            final_eg_prt_list.append(val)

        return final_eg_prt_list
            
#get_valid_ingress_port()
#get_valid_egress_port()
