#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

default_dict = {'name':'test'}
pack_opt = {'fill':'x','expand':True, 'padx':10}

class InpBuilder(tk.Tk):
    def __init__(self):
        super().__init__()

        self.data = dict()
        self.methods = ('Variational Monte Carlo','Diffusion Monte Carlo','Wave function optimization')

        run_name = tk.StringVar()
        run_num  = tk.StringVar()
        sys_file = tk.StringVar()
        ham_file = tk.StringVar()
        wf_file  = tk.StringVar()
        method = tk.StringVar()
        n_blocks = tk.StringVar()
        n_steps  = tk.StringVar()
        timestep = tk.StringVar()
        walkers  = tk.StringVar()
        warmup  = tk.StringVar()
        substeps  = tk.StringVar()

        self.make_title()
        self.data_entry("Run name:",run_name,"test",True)
        self.data_entry("Run number:",run_num,"0")
        self.data_entry("System file:",sys_file,".ptcl.xml")
        self.data_entry("Hamiltonian file:",ham_file,".ham.xml")
        self.data_entry("Wave function file:",wf_file,".wfs.xml")

        self.method_label = ttk.Label(self, text="QMC method:")
        self.method_label.pack(pack_opt,pady=(10,0))
        self.method_menu = ttk.OptionMenu(self,method,self.methods[0],*self.methods)
        self.method_menu.pack(pack_opt)

        self.data_entry("Blocks:",n_blocks,"10")
        self.data_entry("Steps:",n_steps,"100")
        self.data_entry("Substeps:",substeps,"1")
        self.data_entry("Warmup steps:",warmup,"10")
        self.data_entry("Timestep:",timestep,"1.0")
        self.data_entry("Walkers:",walkers,"1")

        self.data['name'] = run_name
        self.data['num']  = run_num
        self.data['sys']  = sys_file
        self.data['ham']  = ham_file
        self.data['wf']   = wf_file
        self.data['method'] = method
        self.data['blocks'] = n_blocks
        self.data['steps']  = n_steps
        self.data['timestep'] = timestep
        self.data['walkers']  = walkers
        self.data['warmup']  = warmup
        self.data['substeps'] = substeps

        self.button = ttk.Button(self, text=f"Save file")
        self.button['command']= self.print_file
        self.button.pack(pack_opt,pady=(20,10))

    def make_title(self):
        self.label = ttk.Label(self,text='Input generator for QMCPack', font = ('Helvetica',14),padding=5).pack()
        self.label2= ttk.Label(self,text='The files with information on the system and wave function are' 
             ' assumed to be created with the pw2qmcpack script!', font = ('Helvetica',12),padding=5, wraplength=500).pack()
        self.title("QMCPack input generator")

    def data_entry(self,descr,variable,default=None,toFocus=False):
        label = ttk.Label(self, text=descr)
        if default:
            variable.set(default)
        label.pack(pack_opt,pady=(10,0))
        entry = ttk.Entry(self, textvariable=variable)
        entry.pack(pack_opt)
        if toFocus:
            entry.focus()

    def print_file(self):
        name = self.data['name'].get()
        num = self.data['num'].get()
        sys = self.data['sys'].get()
        ham = self.data['ham'].get()
        wf = self.data['wf'].get()
        method = self.data['method'].get()
        blocks = self.data['blocks'].get()
        steps  = self.data['steps'].get()
        timestep = self.data['timestep'].get()
        walkers  = self.data['walkers'].get()
        warmup  = self.data['warmup'].get()
        substeps  = self.data['substeps'].get()

        with open(name+'.in.xml','w') as fileout:
            fileout.write(f'<?xml version="1.0"?>\n')
            fileout.write(f'<simulation>\n')
            fileout.write(f'\n')
            fileout.write(f'  <project id={name} series={num}>\n')
            fileout.write(f'    <application name="qmcpack" role="molecu" class="serial" version="1.0"/>\n')
            fileout.write(f'  </project>\n')
            fileout.write(f'\n')
            fileout.write(f'  <include href="{sys}"/>\n')
            fileout.write(f'  <include href="{ham}"/>\n')
            fileout.write(f'  <include href="{wf}"/>\n')
            fileout.write(f'\n')
            if method=="Variational Monte Carlo":
                fileout.write(f'  <qmc method="vmc" move="pbyp" checkpoint="0">\n')
                fileout.write(f'    <parameter name="warmupsteps">  {warmup:4}  </parameter>\n')
                fileout.write(f'    <parameter name="blocks"     >  {blocks:4}  </parameter>\n')
                fileout.write(f'    <parameter name="steps"      >  {steps:4}  </parameter>\n')
                fileout.write(f'    <parameter name="substeps"   >  {substeps:4}  </parameter> \n')
                fileout.write(f'    <parameter name="timestep"   >  {timestep:4}  </parameter>\n')
                fileout.write(f'    <parameter name="walkers"    >  {walkers:4}  </parameter>\n')
                fileout.write(f'    <parameter name="usedrift"   >   yes  </parameter>\n')
                fileout.write(f'  </qmc>\n')
            elif method=="Diffusion Monte Carlo":
                fileout.write(f'  <qmc method="dmc" move="pbyp" checkpoint="0">\n')
                fileout.write(f'    <parameter name="warmupsteps">  {warmup:4}  </parameter>\n')
                fileout.write(f'    <parameter name="blocks"     >  {blocks:4}  </parameter>\n')
                fileout.write(f'    <parameter name="steps"      >  {steps:4}  </parameter>\n')
                fileout.write(f'    <parameter name="substeps"   >  {substeps:4}  </parameter> \n')
                fileout.write(f'    <parameter name="timestep"   >  {timestep:4}  </parameter>\n')
                fileout.write(f'    <parameter name="walkers"    >  {walkers:4}  </parameter>\n')
                fileout.write(f'  </qmc>\n')
            elif method=="Wave function optimization":
                fileout.write(f'  <loop max="10">\n')
                fileout.write(f'    <qmc method="linear" move="pbyp" checkpoint="0">\n')
                fileout.write(f'      <parameter name="warmupsteps">  {warmup:4}  </parameter>\n')
                fileout.write(f'      <parameter name="blocks"     >  {blocks:4}  </parameter>\n')
                fileout.write(f'      <parameter name="steps"      >  {steps:4}  </parameter>\n')
                fileout.write(f'      <parameter name="substeps"   >  {substeps:4}  </parameter> \n')
                fileout.write(f'      <parameter name="timestep"   >  {timestep:4}  </parameter>\n')
                fileout.write(f'      <parameter name="walkers"    >  {walkers:4}  </parameter>\n')
                fileout.write(f'      <parameter name="usedrift"   >   no   </parameter>\n')
                fileout.write(f'      <parameter name="MinMethod"  >   OneShiftOnly  </parameter>\n')
                fileout.write(f'      <parameter name="minwalkers" >           0.01  </parameter>\n')
                fileout.write(f'      <parameter name="samples"             >  9999  </parameter>\n')
                fileout.write(f'      <parameter name="stepsbetweensamples" >     1  </parameter>\n')
                fileout.write(f'      <cost name="energy"              > 0.7 </cost>\n')
                fileout.write(f'      <cost name="unreweightedvariance"> 0.3 </cost>\n')
                fileout.write(f'      <cost name="reweightedvariance"  > 0.0 </cost>\n')
                #fileout.write(f'      \n')
                fileout.write(f'    </qmc>\n')
                fileout.write(f'  <\loop>\n')
            else:
                raise ValueError("Something very wrong is happening when choosing the QMC method.")
            fileout.write(f'\n')
            fileout.write(f'</simulation>\n')
        print(f"Output written to the {name+'.in.xml'} file!")


def main():
    app = InpBuilder()
    app.mainloop()

if __name__ == '__main__':
    main()
