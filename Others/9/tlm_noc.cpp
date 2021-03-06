/********************************************************************************
        MPSoCBench Benchmark Suite
        Authors: Liana Duenha
        Supervisor: Rodolfo Azevedo
        Date: July-2012
        www.archc.org/benchs/mpsocbench

        Computer Systems Laboratory (LSC)
        IC-UNICAMP
        http://www.lsc.ic.unicamp.br/


        This source code is part of the MPSoCBench Benchmark Suite, which is a
free
        source-code benchmark for evaluation of Electronic Systemc Level
designs.
        This benchmark is distributed with hope that it will be useful, but
        without any warranty.

*********************************************************************************/

/******************************************************************************
 * @file      tlm_noc.cpp
 * @author    Liana Duenha
 *
 * @author    The ArchC Team
 *            http://www.archc.org/
 *
 *            Computer Systems Laboratory (LSC)
 *            IC-UNICAMP
 *            http://www.lsc.ic.unicamp.br/
 *
 * @date      01, Feb, 2013
 * @brief     Defines a TLM 2.0 NOC
 *
 *******************************************************************************/

#include "tlm_noc.h"
#include "tlm_node.h"
#include "wrappers_noc.h"

#include "../../defines.h"

#define measures 1

FILE *local_noc_file;
FILE *local_noc_file_csv;
FILE *global_noc_file;

/// Namespace to isolate noc from ArchC
using user::tlm_noc;
using user::tlm_slave_node;
using user::tlm_master_node;
using user::wrapper_master_slave_to_noc;

/// Constructor
tlm_noc::tlm_noc(sc_module_name module_name, int n, int m, int lines,
                 int columns)
    :
#ifdef POWER_SIM
      ps((const char *)module_name, lines * columns),
#endif
      sc_module(module_name) {
  setNumberOfMasters(n);
  setNumberOfSlaves(m);
  setNumberOfPeripherals(n + m);
  setNumberOfLines(lines);
  setNumberOfColumns(columns);
  setNumberOfNodes(getNumberOfLines() * getNumberOfColumns());
  setNumberOfInactiveNodes(getNumberOfNodes() - getNumberOfPeripherals());
  setNumberOfSlaveEmptyNodes(getNumberOfMasters());
  setNumberOfMasterEmptyNodes(getNumberOfSlaves());
  setNumberOfWrappers(getNumberOfNodes());
  create();
  init();
  bindingInternalPorts();
}

void tlm_noc::create() {
  /*
  mesh = new tlm_node*[numberOfLines];
  for (unsigned int i=0; i<numberOfLines; i++)
  {

  mesh[i] = new tlm_node[numberOfColumns];
  }
  */

  std::vector<tlm_node *> *tmp;
  char charBuffer[100];
  for (unsigned int i = 0; i < numberOfLines; i++) {
    tmp = new std::vector<tlm_node *>();
    for (unsigned int j = 0; j < numberOfColumns; j++) {
      snprintf(charBuffer, 100, "tlm_noc_%i_%i", i, j);
      tmp->push_back(new tlm_node(charBuffer));
    }
    mesh.push_back(tmp);
  }
  // (*mesh[i])[j]->counterN

  wrapper = new wrapper_master_slave_to_noc[getNumberOfWrappers()];
  slaveEmptyNodes = new tlm_slave_node[getNumberOfSlaveEmptyNodes()];
  masterEmptyNodes = new tlm_master_node[getNumberOfMasterEmptyNodes()];
}

void tlm_noc::destroyComponents() {

  if (measures) {

    local_noc_file = fopen(LOCAL_FILE_MEASURES_NAME, "a");
    local_noc_file_csv = fopen(LOCAL_FILE_MEASURES_NAME_CSV, "a");
    global_noc_file = fopen(GLOBAL_FILE_MEASURES_NAME, "a");

    // numberOfHops in each wrapper
    long int totalNumberOfHops = 0;
    long int totalNumberOfPackages = 0;
    double averageNumberOfHopsPerPackage = 0;

	fprintf(local_noc_file_csv, "\n ,Nodes(X;Y), X, Y, requests, hops, average (hops per request)");
    for (unsigned int i = 0; i < getNumberOfWrappers(); i++) {
      fprintf(local_noc_file, "\nNode %d,%d-> requests:\t%ld",
              wrapper[i].getX(), wrapper[i].getY(),
              wrapper[i].getNumberOfPackages());
      fprintf(global_noc_file, "\nNode %d,%d-> requests:\t%ld",
              wrapper[i].getX(), wrapper[i].getY(),
              wrapper[i].getNumberOfPackages());

      fprintf(local_noc_file, "\nNode %d,%d-> hops: \t%ld", wrapper[i].getX(),
              wrapper[i].getY(), wrapper[i].getNumberOfHops());
      fprintf(global_noc_file, "\nNode %d,%d-> hops: \t%ld", wrapper[i].getX(),
              wrapper[i].getY(), wrapper[i].getNumberOfHops());

	  // Add by Isabelle Nunes
	  fprintf(local_noc_file_csv, "\n,,%d,%d, %ld, %ld", wrapper[i].getX(), wrapper[i].getY(),
              wrapper[i].getNumberOfPackages(), wrapper[i].getNumberOfHops() );
      // -------------------------------------------------------------------- 
              
      int av = wrapper[i].getNumberOfPackages() != 0
                   ? (int)wrapper[i].getNumberOfHops() /
                         wrapper[i].getNumberOfPackages()
                   : 0;

      fprintf(local_noc_file, "\nNode %d,%d-> average hops per request: \t%d",
              wrapper[i].getX(), wrapper[i].getY(), av);
      fprintf(global_noc_file, "\nNode %d,%d-> average hops per request: \t%d",
              wrapper[i].getX(), wrapper[i].getY(), av);
              
      fprintf(local_noc_file_csv, ",%d",
              av);

      totalNumberOfPackages += wrapper[i].getNumberOfPackages();
      totalNumberOfHops += wrapper[i].getNumberOfHops();
    }

	// Add by Isabelle Nunes
	fprintf(local_noc_file_csv, "\n\nTotal Number of Packages:,%ld",
            totalNumberOfPackages);
    fprintf(local_noc_file_csv, "\nTotal Number of Hops:,%ld", totalNumberOfHops);
    fprintf(local_noc_file_csv, "\nAverage Number of Hops per package:,%d",
            (int)(totalNumberOfHops / totalNumberOfPackages));
    // -------------------------------------------------------------------- 
      
    fprintf(local_noc_file, "\nTotal Number of Packages:\t%ld",
            totalNumberOfPackages);
    fprintf(local_noc_file, "\nTotal Number of Hops:\t%ld", totalNumberOfHops);
    fprintf(local_noc_file, "\nAverage Number of Hops per package:\t%d",
            (int)(totalNumberOfHops / totalNumberOfPackages));

    fprintf(global_noc_file, "\nTotal Number of Packages:\t%ld",
            totalNumberOfPackages);
    fprintf(global_noc_file, "\nTotal Number of Hops:\t%ld", totalNumberOfHops);
    fprintf(global_noc_file, "\nAverage Number of Hops per package:\t%d",
            (int)(totalNumberOfHops / totalNumberOfPackages));

    printf("\nTotal Number of Packages:\t%ld", totalNumberOfPackages);
    printf("\nTotal Number of Hops:\t%ld", totalNumberOfHops);
    printf("\nAverage Number of Hops per package:\t%d",
           (int)(totalNumberOfHops / totalNumberOfPackages));
	
	// Add by Isabelle Nunes
    fprintf(local_noc_file_csv, "\n\nNetwork Traffic Data per Node:");
    fprintf(local_noc_file_csv, "\n ,Nodes(X;Y)");
    fprintf(local_noc_file_csv, "\n ,,X, Y, Port, Packages through");
    // --------------------------------------------------------------------
    
    fprintf(local_noc_file, "\nNetwork Traffic Data per Node:");
    fprintf(global_noc_file, "\nNetwork Traffic Data per Node:");

    for (unsigned int i = 0; i < numberOfLines; i++) {
      for (unsigned int j = 0; j < numberOfColumns; j++) {
        fprintf(local_noc_file,
                "\nNode %d,%d-> packages through north port: \t%d", i, j,
                (*mesh[i])[j]->counterN);
        fprintf(local_noc_file,
                "\nNode %d,%d-> packages through south port: \t%d", i, j,
                (*mesh[i])[j]->counterS);
        fprintf(local_noc_file,
                "\nNode %d,%d-> packages through east port: \t%d", i, j,
                (*mesh[i])[j]->counterE);
        fprintf(local_noc_file,
                "\nNode %d,%d-> packages through west port: \t%d", i, j,
                (*mesh[i])[j]->counterW);
        fprintf(local_noc_file,
                "\nNode %d,%d-> packages through local port: \t%d", i, j,
                (*mesh[i])[j]->counterL);
        
        // Add by Isabelle Nunes
        fprintf(local_noc_file_csv, "\n ,,%d,%d, north, %d", i, j,(*mesh[i])[j]->counterN);
        fprintf(local_noc_file_csv,"\n ,,%d,%d, south, %d", i, j, (*mesh[i])[j]->counterS);
        fprintf(local_noc_file_csv, "\n ,,%d,%d, east, %d", i, j, (*mesh[i])[j]->counterE);
        fprintf(local_noc_file_csv, "\n ,,%d,%d, west, %d", i, j,(*mesh[i])[j]->counterW);
        fprintf(local_noc_file_csv, "\n ,,%d,%d, local, %d", i, j, (*mesh[i])[j]->counterL);
        // --------------------------------------------------------------------               
        
        fprintf(global_noc_file,
                "\nNode %d,%d-> packages through north port: \t%d", i, j,
                (*mesh[i])[j]->counterN);
        fprintf(global_noc_file,
                "\nNode %d,%d-> packages through south port: \t%d", i, j,
                (*mesh[i])[j]->counterS);
        fprintf(global_noc_file,
                "\nNode %d,%d-> packages through east port: \t%d", i, j,
                (*mesh[i])[j]->counterE);
        fprintf(global_noc_file,
                "\nNode %d,%d-> packages through west port: \t%d", i, j,
                (*mesh[i])[j]->counterW);
        fprintf(global_noc_file,
                "\nNode %d,%d-> packages through local port: \t%d", i, j,
                (*mesh[i])[j]->counterL);
      }
    }

    fclose(global_noc_file);
    fclose(local_noc_file);
    fclose(local_noc_file_csv);
  }

  for (unsigned int i = 0; i < numberOfLines; i++) {
    for (unsigned int j = 0; j < numberOfColumns; j++)
      delete (*mesh[i])[j];
    delete mesh[i];
  }

  delete[] masterEmptyNodes;
  delete[] slaveEmptyNodes;
  delete[] wrapper;
}
tlm_noc::~tlm_noc() {}

void tlm_noc::init() {

  // Nodes
  for (unsigned int i = 0; i < numberOfLines; i++) {
    for (unsigned int j = 0; j < numberOfColumns; j++) {
      (*mesh[i])[j]->setStatus(OFF);
#ifdef POWER_SIM
      (*mesh[i])[j]->ps = &ps;
#endif
    }
  }

  // EmptyNodes
  for (unsigned int i = 0; i < getNumberOfSlaveEmptyNodes(); i++) {
    slaveEmptyNodes[i].setStatus(OFF);
  }
  for (unsigned int i = 0; i < getNumberOfMasterEmptyNodes(); i++) {
    masterEmptyNodes[i].setStatus(OFF);
  }
  // Wrappers
  for (unsigned int i = 0; i < getNumberOfWrappers(); i++) {
    wrapper[i].setStatus(OFF);
  }
}

void tlm_noc::bindingInternalPorts() {

  unsigned int wrMS = 0;

  for (unsigned int i = 0; i < getNumberOfLines(); i++) {
    for (unsigned int j = 0; j < getNumberOfColumns(); j++) {
      // status
      if (wrMS < getNumberOfPeripherals()) {
        (*mesh[i])[j]->setStatus(ON);
        wrapper[wrMS].setStatus(ON);
      }

      // position
      wrapper[wrMS].setX(i);
      wrapper[wrMS].setY(j);
      (*mesh[i])[j]->setX(i);
      (*mesh[i])[j]->setY(j);

      // bind node and wrapper
      (*mesh[i])[j]->LOCAL_init_socket.bind(wrapper[wrMS].NODE_target_socket);
      wrapper[wrMS].NODE_init_socket.bind((*mesh[i])[j]->LOCAL_target_socket);

      wrMS++;

      // binding internal ports
      if (j < numberOfColumns - 1) {
        if (NOC_DEBUG)
          printf("\nBinding E init socket of node %d,%d and W target socket of "
                 "node %d,%d",
                 i, j, i, j + 1);
        (*mesh[i])[j]->E_init_socket.bind((*mesh[i])[j + 1]->W_target_socket);

      } else {
        if (NOC_DEBUG)
          printf("\nBinding E init socket and E target socket of node %d,%d", i,
                 j);
        (*mesh[i])[j]->E_init_socket.bind((*mesh[i])[j]->E_target_socket);
      }
      if (j > 0) {
        if (NOC_DEBUG)
          printf("\nBinding W init socket of node %d,%d and E target socket of "
                 "node %d,%d",
                 i, j, i, j - 1);
        (*mesh[i])[j]->W_init_socket.bind((*mesh[i])[j - 1]->E_target_socket);

      } else {
        if (NOC_DEBUG)
          printf("\nBinding W init socket and W target socket of node %d,%d", i,
                 j);
        (*mesh[i])[j]->W_init_socket.bind((*mesh[i])[j]->W_target_socket);
      }

      if (i > 0) {
        if (NOC_DEBUG)
          printf("\nBinding N init socket of node %d,%d and S target socket of "
                 "node %d,%d",
                 i, j, i - 1, j);
        (*mesh[i])[j]->N_init_socket.bind((*mesh[i - 1])[j]->S_target_socket);

      } else {
        if (NOC_DEBUG)
          printf("\nBinding N init socket and N target socket of node %d,%d", i,
                 j);
        (*mesh[i])[j]->N_init_socket.bind((*mesh[i])[j]->N_target_socket);
      }

      if (i < numberOfLines - 1) {
        if (NOC_DEBUG)
          printf("\nBinding S init socket of node %d,%d and N target socket of "
                 "node %d,%d",
                 i, j, i + 1, j);
        (*mesh[i])[j]->S_init_socket.bind((*mesh[i + 1])[j]->N_target_socket);

      } else {
        if (NOC_DEBUG)
          printf("\nBinding S init socket and S target socket of node %d,%d", i,
                 j);
        (*mesh[i])[j]->S_init_socket.bind((*mesh[i])[j]->S_target_socket);
      }
    }
  }
}

void tlm_noc::preparingRoutingTable() {
  for (int i = 0; i < getNumberOfWrappers(); i++)
    wrapper[i].tableOfRouts.copyFrom(tableOfRouts);
}

inline void tlm_noc::setNumberOfMasters(unsigned int n) {
  this->numberOfMasters = n;
}
inline void tlm_noc::setNumberOfSlaves(unsigned int m) {
  this->numberOfSlaves = m;
}
inline void tlm_noc::setNumberOfMasterEmptyNodes(unsigned int n) {
  this->numberOfMasterEmptyNodes = n;
}
inline void tlm_noc::setNumberOfSlaveEmptyNodes(unsigned int m) {
  this->numberOfSlaveEmptyNodes = m;
}
inline void tlm_noc::setNumberOfPeripherals(unsigned int n) {
  this->numberOfPeripherals = n;
}
inline void tlm_noc::setNumberOfInactiveNodes(unsigned int n) {
  this->numberOfInactiveNodes = n;
}
inline void tlm_noc::setNumberOfLines(unsigned int n) {
  this->numberOfLines = n;
}
inline void tlm_noc::setNumberOfColumns(unsigned int n) {
  this->numberOfColumns = n;
}
inline void tlm_noc::setNumberOfNodes(unsigned int n) {
  this->numberOfNodes = n;
}

inline void tlm_noc::setNumberOfWrappers(unsigned int n) {
  this->numberOfWrappers = n;
}

inline unsigned int tlm_noc::getNumberOfMasters() {
  return this->numberOfMasters;
}
inline unsigned int tlm_noc::getNumberOfMasterEmptyNodes() {
  return this->numberOfMasterEmptyNodes;
}
inline unsigned int tlm_noc::getNumberOfSlaves() {
  return this->numberOfSlaves;
}
inline unsigned int tlm_noc::getNumberOfSlaveEmptyNodes() {
  return this->numberOfSlaveEmptyNodes;
}
inline unsigned int tlm_noc::getNumberOfPeripherals() {
  return this->numberOfPeripherals;
}
inline unsigned int tlm_noc::getNumberOfInactiveNodes() {
  return this->numberOfInactiveNodes;
}
unsigned int tlm_noc::getNumberOfLines() { return this->numberOfLines; }
unsigned int tlm_noc::getNumberOfColumns() { return this->numberOfColumns; }
unsigned int tlm_noc::getNumberOfNodes() { return this->numberOfNodes; }
inline unsigned int tlm_noc::getNumberOfWrappers() {
  return this->numberOfWrappers;
}

void tlm_noc::print() {
  printf("\nNOC:\n");
  printf("\n%d Lines\n", getNumberOfLines());
  printf("\n%d Columns\n", getNumberOfColumns());
  printf("\n%d Peripherals\n", getNumberOfPeripherals());
  printf("\n%d Masters\n", getNumberOfMasters());
  printf("\n%d Slaves\n", getNumberOfSlaves());
  printf("\n%d Inactive Nodes\n", getNumberOfInactiveNodes());
  printf("\n%d Slave Empty Nodes\n", getNumberOfSlaveEmptyNodes());
  printf("\n%d Master Empty Nodes\n", getNumberOfMasterEmptyNodes());
  printf("\n%d Wrappers for Masters/Slaves\n", getNumberOfWrappers());

  unsigned int k = getNumberOfLines();
  unsigned int m = getNumberOfColumns();

  printf("\nPrinting mesh!\n");
  for (int i = 0; i < k; i++) {
    for (int j = 0; j < m; j++) {
      printf("\nmesh[%d][%d]: status-> %d  x->%d  y->%d", i, j,
             (*mesh[i])[j]->getStatus(), (*mesh[i])[j]->getX(),
             (*mesh[i])[j]->getY());
    }
  }

  printf("\nPrinting Table of routs!");
  tableOfRouts.print();
}

#ifdef POWER_SIM
void tlm_noc::powersc_connect() { ps.powersc_connect(); }
#endif
