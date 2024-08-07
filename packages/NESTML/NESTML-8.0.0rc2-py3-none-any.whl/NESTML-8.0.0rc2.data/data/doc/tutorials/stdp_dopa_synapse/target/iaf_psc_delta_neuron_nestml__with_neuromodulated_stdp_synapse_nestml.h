
/**
 *  iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml.h
 *
 *  This file is part of NEST.
 *
 *  Copyright (C) 2004 The NEST Initiative
 *
 *  NEST is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  NEST is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with NEST.  If not, see <http://www.gnu.org/licenses/>.
 *
 *  Generated from NESTML at time: 2024-06-03 15:14:04.205192
**/
#ifndef IAF_PSC_DELTA_NEURON_NESTML__WITH_NEUROMODULATED_STDP_SYNAPSE_NESTML
#define IAF_PSC_DELTA_NEURON_NESTML__WITH_NEUROMODULATED_STDP_SYNAPSE_NESTML

#ifndef HAVE_LIBLTDL
#error "NEST was compiled without support for dynamic loading. Please install libltdl and recompile NEST."
#endif

// C++ includes:
#include <cmath>

#include "config.h"

// Includes from nestkernel:
#include "structural_plasticity_node.h"
#include "connection.h"
#include "dict_util.h"
#include "event.h"
#include "nest_types.h"
#include "ring_buffer.h"
#include "universal_data_logger.h"

// Includes from sli:
#include "dictdatum.h"

namespace nest
{
namespace iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names
{
    const Name _V_m( "V_m" );
    const Name _refr_t( "refr_t" );
    const Name _is_refractory( "is_refractory" );
    const Name _post_tr__for_neuromodulated_stdp_synapse_nestml( "post_tr__for_neuromodulated_stdp_synapse_nestml" );
    const Name _tau_m( "tau_m" );
    const Name _C_m( "C_m" );
    const Name _refr_T( "refr_T" );
    const Name _tau_syn( "tau_syn" );
    const Name _E_L( "E_L" );
    const Name _V_reset( "V_reset" );
    const Name _V_th( "V_th" );
    const Name _V_min( "V_min" );
    const Name _I_e( "I_e" );
    const Name _tau_tr_post__for_neuromodulated_stdp_synapse_nestml( "tau_tr_post__for_neuromodulated_stdp_synapse_nestml" );
}
}




#include "nest_time.h"
  typedef size_t nest_port_t;
  typedef size_t nest_rport_t;

// entry in the spiking history
class histentry__iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml
{
public:
  histentry__iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml( double t,
double post_tr__for_neuromodulated_stdp_synapse_nestml,
size_t access_counter )
  : t_( t )
  , post_tr__for_neuromodulated_stdp_synapse_nestml_( post_tr__for_neuromodulated_stdp_synapse_nestml )
  , access_counter_( access_counter )
  {
  }

  double t_;              //!< point in time when spike occurred (in ms)
   double post_tr__for_neuromodulated_stdp_synapse_nestml_;
  size_t access_counter_; //!< access counter to enable removal of the entry, once all neurons read it
};

/* BeginDocumentation
  Name: iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml

  Description:

    """
  iaf_psc_delta - Current-based leaky integrate-and-fire neuron model with delta-kernel post-synaptic currents###########################################################################################################

  Description
  +++++++++++

  iaf_psc_delta is an implementation of a leaky integrate-and-fire model
  where the potential jumps on each spike arrival.

  The threshold crossing is followed by an absolute refractory period
  during which the membrane potential is clamped to the resting potential.

  Spikes arriving while the neuron is refractory, are discarded by
  default. If the property ``with_refr_input`` is set to true, such
  spikes are added to the membrane potential at the end of the
  refractory period, dampened according to the interval between
  arrival and end of refractoriness.

  The general framework for the consistent formulation of systems with
  neuron like dynamics interacting by point events is described in
  [1]_.  A flow chart can be found in [2]_.


  References
  ++++++++++

  .. [1] Rotter S,  Diesmann M (1999). Exact simulation of
         time-invariant linear systems with applications to neuronal
         modeling. Biologial Cybernetics 81:381-402.
         DOI: https://doi.org/10.1007/s004220050570
  .. [2] Diesmann M, Gewaltig M-O, Rotter S, & Aertsen A (2001). State
         space analysis of synchronous spiking in cortical neural
         networks. Neurocomputing 38-40:565-571.
         DOI: https://doi.org/10.1016/S0925-2312(01)00409-X


  See also
  ++++++++

  iaf_psc_alpha, iaf_psc_exp
  """


  Parameters:
  The following parameters can be set in the status dictionary.
tau_m [ms]  Membrane time constant
C_m [pF]  Capacity of the membrane
refr_T [ms]  Duration of refractory period
tau_syn [ms]  Time constant of synaptic current
E_L [mV]  Resting membrane potential
V_reset [mV]  Reset potential of the membrane
V_th [mV]  Spike threshold
V_min [mV]  Absolute lower value for the membrane potential
I_e [pA]  constant external input current
tau_tr_post__for_neuromodulated_stdp_synapse_nestml [ms]  STDP time constant for weight changes caused by post-before-pre spike pairings.


  Dynamic state variables:
V_m [mV]  Membrane potential
refr_t [ms]  Refractory period timer


  Sends: nest::SpikeEvent

  Receives: Spike, Current, DataLoggingRequest
*/

// Register the neuron model
void register_iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml( const std::string& name );

class iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml : public nest::StructuralPlasticityNode
{
public:
  /**
   * The constructor is only used to create the model prototype in the model manager.
  **/
  iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml();

  /**
   * The copy constructor is used to create model copies and instances of the model.
   * @node The copy constructor needs to initialize the parameters and the state.
   *       Initialization of buffers and interal variables is deferred to
   *       @c init_buffers_() and @c pre_run_hook() (or calibrate() in NEST 3.3 and older).
  **/
  iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml(const iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml &);

  /**
   * Destructor.
  **/
  ~iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml() override;

  // -------------------------------------------------------------------------
  //   Import sets of overloaded virtual functions.
  //   See: Technical Issues / Virtual Functions: Overriding, Overloading,
  //        and Hiding
  // -------------------------------------------------------------------------

  using nest::Node::handles_test_event;
  using nest::Node::handle;

  /**
   * Used to validate that we can send nest::SpikeEvent to desired target:port.
  **/
  nest_port_t send_test_event(nest::Node& target, nest_rport_t receptor_type, nest::synindex, bool) override;


  // -------------------------------------------------------------------------
  //   Functions handling incoming events.
  //   We tell nest that we can handle incoming events of various types by
  //   defining handle() for the given event.
  // -------------------------------------------------------------------------


  void handle(nest::SpikeEvent &) override;        //! accept spikes
  void handle(nest::CurrentEvent &) override;      //! accept input current

  void handle(nest::DataLoggingRequest &) override;//! allow recording with multimeter
  nest_port_t handles_test_event(nest::SpikeEvent&, nest_port_t) override;
  nest_port_t handles_test_event(nest::CurrentEvent&, nest_port_t) override;
  nest_port_t handles_test_event(nest::DataLoggingRequest&, nest_port_t) override;

  // -------------------------------------------------------------------------
  //   Functions for getting/setting parameters and state values.
  // -------------------------------------------------------------------------

  void get_status(DictionaryDatum &) const override;
  void set_status(const DictionaryDatum &) override;


  // support for spike archiving

  /**
   * \fn void get_history(long t1, long t2,
   * std::deque<Archiver::histentry__>::iterator* start,
   * std::deque<Archiver::histentry__>::iterator* finish)
   * return the spike times (in steps) of spikes which occurred in the range
   * (t1,t2].
   * XXX: two underscores to differentiate it from nest::Node::get_history()
   */
  void get_history__( double t1,
    double t2,
    std::deque< histentry__iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml >::iterator* start,
    std::deque< histentry__iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml >::iterator* finish );

  /**
   * Register a new incoming STDP connection.
   *
   * t_first_read: The newly registered synapse will read the history entries
   * with t > t_first_read.
   */
  void register_stdp_connection( double t_first_read, double delay );
  // -------------------------------------------------------------------------
  //   Getters/setters for state block
  // -------------------------------------------------------------------------

  inline double get_V_m() const
  {
    return S_.V_m;
  }

  inline void set_V_m(const double __v)
  {
    S_.V_m = __v;
  }

  inline double get_refr_t() const
  {
    return S_.refr_t;
  }

  inline void set_refr_t(const double __v)
  {
    S_.refr_t = __v;
  }

  inline bool get_is_refractory() const
  {
    return S_.is_refractory;
  }

  inline void set_is_refractory(const bool __v)
  {
    S_.is_refractory = __v;
  }

  inline double get_post_tr__for_neuromodulated_stdp_synapse_nestml() const
  {
    return S_.post_tr__for_neuromodulated_stdp_synapse_nestml;
  }

  inline void set_post_tr__for_neuromodulated_stdp_synapse_nestml(const double __v)
  {
    S_.post_tr__for_neuromodulated_stdp_synapse_nestml = __v;
  }


  // -------------------------------------------------------------------------
  //   Getters/setters for parameters
  // -------------------------------------------------------------------------

  inline double get_tau_m() const
  {
    return P_.tau_m;
  }

  inline void set_tau_m(const double __v)
  {
    P_.tau_m = __v;
  }

  inline double get_C_m() const
  {
    return P_.C_m;
  }

  inline void set_C_m(const double __v)
  {
    P_.C_m = __v;
  }

  inline double get_refr_T() const
  {
    return P_.refr_T;
  }

  inline void set_refr_T(const double __v)
  {
    P_.refr_T = __v;
  }

  inline double get_tau_syn() const
  {
    return P_.tau_syn;
  }

  inline void set_tau_syn(const double __v)
  {
    P_.tau_syn = __v;
  }

  inline double get_E_L() const
  {
    return P_.E_L;
  }

  inline void set_E_L(const double __v)
  {
    P_.E_L = __v;
  }

  inline double get_V_reset() const
  {
    return P_.V_reset;
  }

  inline void set_V_reset(const double __v)
  {
    P_.V_reset = __v;
  }

  inline double get_V_th() const
  {
    return P_.V_th;
  }

  inline void set_V_th(const double __v)
  {
    P_.V_th = __v;
  }

  inline double get_V_min() const
  {
    return P_.V_min;
  }

  inline void set_V_min(const double __v)
  {
    P_.V_min = __v;
  }

  inline double get_I_e() const
  {
    return P_.I_e;
  }

  inline void set_I_e(const double __v)
  {
    P_.I_e = __v;
  }

  inline double get_tau_tr_post__for_neuromodulated_stdp_synapse_nestml() const
  {
    return P_.tau_tr_post__for_neuromodulated_stdp_synapse_nestml;
  }

  inline void set_tau_tr_post__for_neuromodulated_stdp_synapse_nestml(const double __v)
  {
    P_.tau_tr_post__for_neuromodulated_stdp_synapse_nestml = __v;
  }


  // -------------------------------------------------------------------------
  //   Getters/setters for internals
  // -------------------------------------------------------------------------

  inline double get___h() const
  {
    return V_.__h;
  }

  inline void set___h(const double __v)
  {
    V_.__h = __v;
  }
  inline double get___P__V_m__V_m() const
  {
    return V_.__P__V_m__V_m;
  }

  inline void set___P__V_m__V_m(const double __v)
  {
    V_.__P__V_m__V_m = __v;
  }
  inline double get___P__post_tr__for_neuromodulated_stdp_synapse_nestml__post_tr__for_neuromodulated_stdp_synapse_nestml() const
  {
    return V_.__P__post_tr__for_neuromodulated_stdp_synapse_nestml__post_tr__for_neuromodulated_stdp_synapse_nestml;
  }

  inline void set___P__post_tr__for_neuromodulated_stdp_synapse_nestml__post_tr__for_neuromodulated_stdp_synapse_nestml(const double __v)
  {
    V_.__P__post_tr__for_neuromodulated_stdp_synapse_nestml__post_tr__for_neuromodulated_stdp_synapse_nestml = __v;
  }


  /* getters/setters for variables transferred from synapse */
  double get_post_tr__for_neuromodulated_stdp_synapse_nestml( double t, const bool before_increment = true );

  // -------------------------------------------------------------------------
  //   Methods corresponding to event handlers
  // -------------------------------------------------------------------------

  

  // -------------------------------------------------------------------------
  //   Initialization functions
  // -------------------------------------------------------------------------
  void calibrate_time( const nest::TimeConverter& tc ) override;

protected:
  // support for spike archiving

  /**
   * record spike history
   */
  void set_spiketime( nest::Time const& t_sp, double offset = 0.0 );

  /**
   * return most recent spike time in ms
   */
  inline double get_spiketime_ms() const;

  /**
   * clear spike history
   */
  void clear_history();

private:
  void recompute_internal_variables(bool exclude_timestep=false);
  // support for spike archiving

  // number of incoming connections from stdp connectors.
  // needed to determine, if every incoming connection has
  // read the spikehistory for a given point in time
  size_t n_incoming_;

  double max_delay_;

  double last_spike_;

  // spiking history needed by stdp synapses
  std::deque< histentry__iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml > history_;

  // cache for initial values
  double post_tr__for_neuromodulated_stdp_synapse_nestml__iv;

private:

  static const nest_port_t MIN_SPIKE_RECEPTOR = 0;
  static const nest_port_t PORT_NOT_AVAILABLE = -1;

  enum SynapseTypes
  {
    SPIKES = 0,
    MAX_SPIKE_RECEPTOR = 1
  };

  static const size_t NUM_SPIKE_RECEPTORS = MAX_SPIKE_RECEPTOR - MIN_SPIKE_RECEPTOR;



  /**
   * Reset state of neuron.
  **/

  void init_state_internal_();

  /**
   * Reset internal buffers of neuron.
  **/
  void init_buffers_() override;

  /**
   * Initialize auxiliary quantities, leave parameters and state untouched.
  **/
  void pre_run_hook() override;

  /**
   * Take neuron through given time interval
  **/
  void update(nest::Time const &, const long, const long) override;

  // The next two classes need to be friends to access the State_ class/member
  friend class nest::RecordablesMap<iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml>;
  friend class nest::UniversalDataLogger<iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml>;

  /**
   * Free parameters of the neuron.
   *


   *
   * These are the parameters that can be set by the user through @c `node.set()`.
   * They are initialized from the model prototype when the node is created.
   * Parameters do not change during calls to @c update() and are not reset by
   * @c ResetNetwork.
   *
   * @note Parameters_ need neither copy constructor nor @c operator=(), since
   *       all its members are copied properly by the default copy constructor
   *       and assignment operator. Important:
   *       - If Parameters_ contained @c Time members, you need to define the
   *         assignment operator to recalibrate all members of type @c Time . You
   *         may also want to define the assignment operator.
   *       - If Parameters_ contained members that cannot copy themselves, such
   *         as C-style arrays, you need to define the copy constructor and
   *         assignment operator to copy those members.
  **/
  struct Parameters_
  {    
    //!  Membrane time constant
    double tau_m;
    //!  Capacity of the membrane
    double C_m;
    //!  Duration of refractory period
    double refr_T;
    //!  Time constant of synaptic current
    double tau_syn;
    //!  Resting membrane potential
    double E_L;
    //!  Reset potential of the membrane
    double V_reset;
    //!  Spike threshold
    double V_th;
    //!  Absolute lower value for the membrane potential
    double V_min;
    //!  constant external input current
    double I_e;
    //!  STDP time constant for weight changes caused by post-before-pre spike pairings.
    double tau_tr_post__for_neuromodulated_stdp_synapse_nestml;

    /**
     * Initialize parameters to their default values.
    **/
    Parameters_();
  };

  /**
   * Dynamic state of the neuron.
   *
   *
   *
   * These are the state variables that are advanced in time by calls to
   * @c update(). In many models, some or all of them can be set by the user
   * through @c `node.set()`. The state variables are initialized from the model
   * prototype when the node is created. State variables are reset by @c ResetNetwork.
   *
   * @note State_ need neither copy constructor nor @c operator=(), since
   *       all its members are copied properly by the default copy constructor
   *       and assignment operator. Important:
   *       - If State_ contained @c Time members, you need to define the
   *         assignment operator to recalibrate all members of type @c Time . You
   *         may also want to define the assignment operator.
   *       - If State_ contained members that cannot copy themselves, such
   *         as C-style arrays, you need to define the copy constructor and
   *         assignment operator to copy those members.
  **/
  struct State_
  {    
    //!  Membrane potential
    double V_m;
    //!  Refractory period timer
    double refr_t;
    bool is_refractory;
    double post_tr__for_neuromodulated_stdp_synapse_nestml;

    State_();
  };

  struct DelayedVariables_
  {
  };

  /**
   * Internal variables of the neuron.
   *
   *
   *
   * These variables must be initialized by @c pre_run_hook (or calibrate in NEST 3.3 and older), which is called before
   * the first call to @c update() upon each call to @c Simulate.
   * @node Variables_ needs neither constructor, copy constructor or assignment operator,
   *       since it is initialized by @c pre_run_hook() (or calibrate() in NEST 3.3 and older). If Variables_ has members that
   *       cannot destroy themselves, Variables_ will need a destructor.
  **/
  struct Variables_
  {
    double __h;
    double __P__V_m__V_m;
    double __P__post_tr__for_neuromodulated_stdp_synapse_nestml__post_tr__for_neuromodulated_stdp_synapse_nestml;
  };

  /**
   * Buffers of the neuron.
   * Usually buffers for incoming spikes and data logged for analog recorders.
   * Buffers must be initialized by @c init_buffers_(), which is called before
   * @c pre_run_hook() (or calibrate() in NEST 3.3 and older) on the first call to @c Simulate after the start of NEST,
   * ResetKernel or ResetNetwork.
   * @node Buffers_ needs neither constructor, copy constructor or assignment operator,
   *       since it is initialized by @c init_nodes_(). If Buffers_ has members that
   *       cannot destroy themselves, Buffers_ will need a destructor.
  **/
  struct Buffers_
  {
    Buffers_(iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml &);
    Buffers_(const Buffers_ &, iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml &);

    /**
     * Logger for all analog data
    **/
    nest::UniversalDataLogger<iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml> logger_;

    // -----------------------------------------------------------------------
    //   Spike buffers and sums of incoming spikes/currents per timestep
    // -----------------------------------------------------------------------    



    /**
     * Buffer containing the incoming spikes
    **/
    inline std::vector< nest::RingBuffer >& get_spike_inputs_()
    {
        return spike_inputs_;
    }
    std::vector< nest::RingBuffer > spike_inputs_;

    /**
     * Buffer containing the sum of all the incoming spikes
    **/
    inline std::vector< double >& get_spike_inputs_grid_sum_()
    {
        return spike_inputs_grid_sum_;
    }
    std::vector< double > spike_inputs_grid_sum_;

    /**
     * Buffer containing a flag whether incoming spikes have been received on a given port
    **/
    inline std::vector< nest::RingBuffer >& get_spike_input_received_()
    {
        return spike_input_received_;
    }
    std::vector< nest::RingBuffer > spike_input_received_;

    /**
     * Buffer containing a flag whether incoming spikes have been received on a given port
    **/
    inline std::vector< double >& get_spike_input_received_grid_sum_()
    {
        return spike_input_received_grid_sum_;
    }
    std::vector< double > spike_input_received_grid_sum_;

    // -----------------------------------------------------------------------
    //   Continuous-input buffers
    // -----------------------------------------------------------------------

    

    nest::RingBuffer
     I_stim;   //!< Buffer for input (type: pA)

    inline nest::RingBuffer& get_I_stim() {
        return I_stim;
    }

    double I_stim_grid_sum_;
  };

  // -------------------------------------------------------------------------
  //   Getters/setters for inline expressions
  // -------------------------------------------------------------------------
  

  // -------------------------------------------------------------------------
  //   Getters/setters for input buffers
  // -------------------------------------------------------------------------  




  /**
   * Buffer containing the incoming spikes
  **/
  inline std::vector< nest::RingBuffer >& get_spike_inputs_()
  {
      return B_.get_spike_inputs_();
  }

  /**
   * Buffer containing the sum of all the incoming spikes
  **/
  inline std::vector< double >& get_spike_inputs_grid_sum_()
  {
      return B_.get_spike_inputs_grid_sum_();
  }

  /**
   * Buffer containing a flag whether incoming spikes have been received on a given port
  **/
  inline std::vector< nest::RingBuffer >& get_spike_input_received_()
  {
      return B_.get_spike_input_received_();
  }

  /**
   * Buffer containing a flag whether incoming spikes have been received on a given port
  **/
  inline std::vector< double >& get_spike_input_received_grid_sum_()
  {
      return B_.get_spike_input_received_grid_sum_();
  }

inline nest::RingBuffer& get_I_stim() {
    return B_.get_I_stim();
}

  // -------------------------------------------------------------------------
  //   Member variables of neuron model.
  //   Each model neuron should have precisely the following four data members,
  //   which are one instance each of the parameters, state, buffers and variables
  //   structures. Experience indicates that the state and variables member should
  //   be next to each other to achieve good efficiency (caching).
  //   Note: Devices require one additional data member, an instance of the
  //   ``Device`` child class they belong to.
  // -------------------------------------------------------------------------


  Parameters_       P_;        //!< Free parameters.
  State_            S_;        //!< Dynamic state.
  DelayedVariables_ DV_;       //!< Delayed state variables.
  Variables_        V_;        //!< Internal Variables
  Buffers_          B_;        //!< Buffers.

  //! Mapping of recordables names to access functions
  static nest::RecordablesMap<iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml> recordablesMap_;

}; /* neuron iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml */

inline nest_port_t iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml::send_test_event(nest::Node& target, nest_rport_t receptor_type, nest::synindex, bool)
{
  // You should usually not change the code in this function.
  // It confirms that the target of connection @c c accepts @c nest::SpikeEvent on
  // the given @c receptor_type.
  nest::SpikeEvent e;
  e.set_sender(*this);
  return target.handles_test_event(e, receptor_type);
}

inline nest_port_t iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml::handles_test_event(nest::SpikeEvent&, nest_port_t receptor_type)
{
    // You should usually not change the code in this function.
    // It confirms to the connection management system that we are able
    // to handle @c SpikeEvent on port 0. You need to extend the function
    // if you want to differentiate between input ports.
    if (receptor_type != 0)
    {
      throw nest::UnknownReceptorType(receptor_type, get_name());
    }
    return 0;
}

inline nest_port_t iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml::handles_test_event(nest::CurrentEvent&, nest_port_t receptor_type)
{
  // You should usually not change the code in this function.
  // It confirms to the connection management system that we are able
  // to handle @c CurrentEvent on port 0. You need to extend the function
  // if you want to differentiate between input ports.
  if (receptor_type != 0)
  {
    throw nest::UnknownReceptorType(receptor_type, get_name());
  }
  return 0;
}

inline nest_port_t iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml::handles_test_event(nest::DataLoggingRequest& dlr, nest_port_t receptor_type)
{
  // You should usually not change the code in this function.
  // It confirms to the connection management system that we are able
  // to handle @c DataLoggingRequest on port 0.
  // The function also tells the built-in UniversalDataLogger that this node
  // is recorded from and that it thus needs to collect data during simulation.
  if (receptor_type != 0)
  {
    throw nest::UnknownReceptorType(receptor_type, get_name());
  }

  return B_.logger_.connect_logging_device(dlr, recordablesMap_);
}

inline void iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml::get_status(DictionaryDatum &__d) const
{
  // parameters
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_tau_m, get_tau_m());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_C_m, get_C_m());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_refr_T, get_refr_T());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_tau_syn, get_tau_syn());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_E_L, get_E_L());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_V_reset, get_V_reset());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_V_th, get_V_th());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_V_min, get_V_min());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_I_e, get_I_e());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_tau_tr_post__for_neuromodulated_stdp_synapse_nestml, get_tau_tr_post__for_neuromodulated_stdp_synapse_nestml());

  // initial values for state variables in ODE or kernel
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_V_m, get_V_m());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_refr_t, get_refr_t());
  def<bool>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_is_refractory, get_is_refractory());
  def<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_post_tr__for_neuromodulated_stdp_synapse_nestml, get_post_tr__for_neuromodulated_stdp_synapse_nestml());

  StructuralPlasticityNode::get_status( __d );

  (*__d)[nest::names::recordables] = recordablesMap_.get_list();
}

inline void iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml::set_status(const DictionaryDatum &__d)
{
  // parameters
  double tmp_tau_m = get_tau_m();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_tau_m, tmp_tau_m, this);
  double tmp_C_m = get_C_m();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_C_m, tmp_C_m, this);
  double tmp_refr_T = get_refr_T();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_refr_T, tmp_refr_T, this);
  double tmp_tau_syn = get_tau_syn();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_tau_syn, tmp_tau_syn, this);
  double tmp_E_L = get_E_L();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_E_L, tmp_E_L, this);
  double tmp_V_reset = get_V_reset();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_V_reset, tmp_V_reset, this);
  double tmp_V_th = get_V_th();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_V_th, tmp_V_th, this);
  double tmp_V_min = get_V_min();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_V_min, tmp_V_min, this);
  double tmp_I_e = get_I_e();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_I_e, tmp_I_e, this);
  double tmp_tau_tr_post__for_neuromodulated_stdp_synapse_nestml = get_tau_tr_post__for_neuromodulated_stdp_synapse_nestml();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_tau_tr_post__for_neuromodulated_stdp_synapse_nestml, tmp_tau_tr_post__for_neuromodulated_stdp_synapse_nestml, this);

  // initial values for state variables in ODE or kernel
  double tmp_V_m = get_V_m();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_V_m, tmp_V_m, this);
  double tmp_refr_t = get_refr_t();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_refr_t, tmp_refr_t, this);
  bool tmp_is_refractory = get_is_refractory();
  nest::updateValueParam<bool>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_is_refractory, tmp_is_refractory, this);
  double tmp_post_tr__for_neuromodulated_stdp_synapse_nestml = get_post_tr__for_neuromodulated_stdp_synapse_nestml();
  nest::updateValueParam<double>(__d, nest::iaf_psc_delta_neuron_nestml__with_neuromodulated_stdp_synapse_nestml_names::_post_tr__for_neuromodulated_stdp_synapse_nestml, tmp_post_tr__for_neuromodulated_stdp_synapse_nestml, this);

  // We now know that (ptmp, stmp) are consistent. We do not
  // write them back to (P_, S_) before we are also sure that
  // the properties to be set in the parent class are internally
  // consistent.
  StructuralPlasticityNode::set_status(__d);

  // if we get here, temporaries contain consistent set of properties
  set_tau_m(tmp_tau_m);
  set_C_m(tmp_C_m);
  set_refr_T(tmp_refr_T);
  set_tau_syn(tmp_tau_syn);
  set_E_L(tmp_E_L);
  set_V_reset(tmp_V_reset);
  set_V_th(tmp_V_th);
  set_V_min(tmp_V_min);
  set_I_e(tmp_I_e);
  set_tau_tr_post__for_neuromodulated_stdp_synapse_nestml(tmp_tau_tr_post__for_neuromodulated_stdp_synapse_nestml);
  set_V_m(tmp_V_m);
  set_refr_t(tmp_refr_t);
  set_is_refractory(tmp_is_refractory);
  set_post_tr__for_neuromodulated_stdp_synapse_nestml(tmp_post_tr__for_neuromodulated_stdp_synapse_nestml);





  // recompute internal variables in case they are dependent on parameters or state that might have been updated in this call to set_status()
  recompute_internal_variables();
};



#endif /* #ifndef IAF_PSC_DELTA_NEURON_NESTML__WITH_NEUROMODULATED_STDP_SYNAPSE_NESTML */
