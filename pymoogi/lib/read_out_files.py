import numpy as np
import re

def out2_abfind(file):
    # read filename from commandline
    with open(file, 'r') as fh:
        data = fh.readlines()

    line_data=np.zeros((1,8),dtype=float)

    for line in data:
        line=re.split('\s+',line.strip())

        try:
            line=np.array(line,dtype=float)
            line_data=np.append(line_data,np.array([line]),axis=0)
        except:
            pass

    return line_data[1:,:]
 
def out2_synth(file):
    #split into blocks
    with open(file, 'r') as fh:
        data_all = fh.read().split("ALL")
    #first element is always empty, remove it
    data_all.pop(0)

    out2_tab=[]
    header_line =np.zeros((1,4))

    # Find line that matches format header_line
    for data in data_all:
        ax=[]
        isotopes=[]
        flux=[]

        for line in filter(None, data.split("\n")):
            line_list  = line.split()
            #Find values for x axis
            try:
                np.array(line_list,dtype=float)
                if len(line_list)>1:
                    header_line[:]=np.array(line_list,dtype=float)
                    head = np.array(line_list,dtype=float)
                    break  # exit with first line found
            except:
                pass

            #Find model
            if line_list[0] =='MODEL:':
                model = " ".join(line.split(":")[1].split())

            #Find abundances
            if line_list[0]=='element':
                el= line.strip().split(":")[0].strip().split(" ")[-1]
                ab= line.strip().split(":")[1].strip().split(" ")[-1]
                ax.append([el, ab])
            #Find isotopes
            if line_list[0]=='Isotopic':
                isot =  line.strip().split(":")[1].strip().split("=")[0].strip()
                ratio= line.strip().split(":")[1].strip().split("=")[-1].strip()
                isotopes.append([isot, ratio])

        for line in  filter(None, data.split("\n")):
            line_list  = line.split()
            #Find all lines that match format data_line
            try:
                flux.append(np.array(line_list,dtype=float))
            except:
                pass

        # remove first element of the list
        flux.pop(0)

        # flatten list of lists
        # http://stackoverflow.com/questions/952914/
        flux = [item for sublist in flux for item in sublist]
        dline=(head,model,ax,isotopes,1.-np.array(flux))
        out2_tab.append(dline)
    return out2_tab

def out3_synth(file):
    # like out2
    with open(file, 'r') as fh:
        data_all = fh.read().split("the number of")
    data_all.pop(0)

    tab_out3=[]

    for data in data_all:
        flux = []
        for line in filter(None,data.split("\n")):
            line_list=line.split()
            try:
                np.array(line_list,dtype=float)
                flux.append(line_list)
            except:
                pass

        tab_out3.append((np.asarray(flux)[:,0], np.asarray(flux)[:,1]))

    return tab_out3
