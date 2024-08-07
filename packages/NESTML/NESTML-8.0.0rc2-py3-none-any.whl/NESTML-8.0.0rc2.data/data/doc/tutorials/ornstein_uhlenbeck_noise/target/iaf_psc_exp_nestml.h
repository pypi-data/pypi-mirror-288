
/**
 *  iaf_psc_exp_nestml.h
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
 *  Generated from NESTML at time: 2024-04-04 08:45:44.097960
**/
#ifndef IAF_PSC_EXP_NESTML
#define IAF_PSC_EXP_NESTML

#ifndef HAVE_LIBLTDL
#error "NEST was compiled without support for dynamic loading. Please install libltdl and recompile NEST."
#endif

// C++ includes:
#include <cmath>

#include "config.h"

// Includes for random number generator
#include <random>

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
namespace iaf_psc_exp_nestml_names
{
    const Name _V_m( "V_m" );
    const Name _I_noise( "I_noise" );
    const Name _psc_kernel__X__spikes( "psc_kernel__X__spikes" );
    const Name _E_L( "E_L" );
    const Name _I_e( "I_e" );
    const Name _tau_m( "tau_m" );
    const Name _tau_syn( "tau_syn" );
    const Name _C_m( "C_m" );
    const Name _V_theta( "V_theta" );
    const Name _mean_noise( "mean_noise" );
    const Name _sigma_noise( "sigma_noise" );
    const Name _tau_noise( "tau_noise" );
}
}




#include "nest_time.h"
  typedef size_t nest_port_t;
  typedef size_t nest_rport_t;

/* BeginDocumentation
  Name: iaf_psc_exp_nestml

  Description:

    

  Parameters:
  The following parameters can be set in the status dictionary.
E_L [mV]  resting potential
I_e [pA]  constant external input current
tau_m [ms]  membrane time constant
tau_syn [ms]  synaptic time constant
C_m [pF]  membrane capacitance
V_theta [mV]  threshold potential
mean_noise [pA]  mean of the noise current
sigma_noise [pA]  standard deviation of the noise current
tau_noise [ms]  time constant of the noise process


  Dynamic state variables:


  Sends: nest::SpikeEvent

  Receives: Spike,  DataLoggingRequest
*/

// Register the neuron model
void register_iaf_psc_exp_nestml( const std::string& name );

class iaf_psc_exp_nestml : public nest::StructuralPlasticityNode
{
public:
  /**
   * The constructor is only used to create the model prototype in the model manager.
  **/
  iaf_psc_exp_nestml();

  /**
   * The copy constructor is used to create model copies and instances of the model.
   * @node The copy constructor needs to initialize the parameters and the state.
   *       Initialization of buffers and interal variables is deferred to
   *       @c init_buffers_() and @c pre_run_hook() (or calibrate() in NEST 3.3 and older).
  **/
  iaf_psc_exp_nestml(const iaf_psc_exp_nestml &);

  /**
   * Destructor.
  **/
  ~iaf_psc_exp_nestml() override;

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

  void handle(nest::DataLoggingRequest &) override;//! allow recording with multimeter
  nest_port_t handles_test_event(nest::SpikeEvent&, nest_port_t) override;
  nest_port_t handles_test_event(nest::DataLoggingRequest&, nest_port_t) override;

  // -------------------------------------------------------------------------
  //   Functions for getting/setting parameters and state values.
  // -------------------------------------------------------------------------

  void get_status(DictionaryDatum &) const override;
  void set_status(const DictionaryDatum &) override;


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

  inline double get_I_noise() const
  {
    return S_.I_noise;
  }

  inline void set_I_noise(const double __v)
  {
    S_.I_noise = __v;
  }

  inline double get_psc_kernel__X__spikes() const
  {
    return S_.psc_kernel__X__spikes;
  }

  inline void set_psc_kernel__X__spikes(const double __v)
  {
    S_.psc_kernel__X__spikes = __v;
  }


  // -------------------------------------------------------------------------
  //   Getters/setters for parameters
  // -------------------------------------------------------------------------

  inline double get_E_L() const
  {
    return P_.E_L;
  }

  inline void set_E_L(const double __v)
  {
    P_.E_L = __v;
  }

  inline double get_I_e() const
  {
    return P_.I_e;
  }

  inline void set_I_e(const double __v)
  {
    P_.I_e = __v;
  }

  inline double get_tau_m() const
  {
    return P_.tau_m;
  }

  inline void set_tau_m(const double __v)
  {
    P_.tau_m = __v;
  }

  inline double get_tau_syn() const
  {
    return P_.tau_syn;
  }

  inline void set_tau_syn(const double __v)
  {
    P_.tau_syn = __v;
  }

  inline double get_C_m() const
  {
    return P_.C_m;
  }

  inline void set_C_m(const double __v)
  {
    P_.C_m = __v;
  }

  inline double get_V_theta() const
  {
    return P_.V_theta;
  }

  inline void set_V_theta(const double __v)
  {
    P_.V_theta = __v;
  }

  inline double get_mean_noise() const
  {
    return P_.mean_noise;
  }

  inline void set_mean_noise(const double __v)
  {
    P_.mean_noise = __v;
  }

  inline double get_sigma_noise() const
  {
    return P_.sigma_noise;
  }

  inline void set_sigma_noise(const double __v)
  {
    P_.sigma_noise = __v;
  }

  inline double get_tau_noise() const
  {
    return P_.tau_noise;
  }

  inline void set_tau_noise(const double __v)
  {
    P_.tau_noise = __v;
  }


  // -------------------------------------------------------------------------
  //   Getters/setters for internals
  // -------------------------------------------------------------------------

  inline double get_A_noise() const
  {
    return V_.A_noise;
  }

  inline void set_A_noise(const double __v)
  {
    V_.A_noise = __v;
  }
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
  inline double get___P__V_m__psc_kernel__X__spikes() const
  {
    return V_.__P__V_m__psc_kernel__X__spikes;
  }

  inline void set___P__V_m__psc_kernel__X__spikes(const double __v)
  {
    V_.__P__V_m__psc_kernel__X__spikes = __v;
  }
  inline double get___P__psc_kernel__X__spikes__psc_kernel__X__spikes() const
  {
    return V_.__P__psc_kernel__X__spikes__psc_kernel__X__spikes;
  }

  inline void set___P__psc_kernel__X__spikes__psc_kernel__X__spikes(const double __v)
  {
    V_.__P__psc_kernel__X__spikes__psc_kernel__X__spikes = __v;
  }


  // -------------------------------------------------------------------------
  //   Initialization functions
  // -------------------------------------------------------------------------
  void calibrate_time( const nest::TimeConverter& tc ) override;

protected:

private:
  void recompute_internal_variables(bool exclude_timestep=false);

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
  friend class nest::RecordablesMap<iaf_psc_exp_nestml>;
  friend class nest::UniversalDataLogger<iaf_psc_exp_nestml>;

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
    //!  resting potential
    double E_L;
    //!  constant external input current
    double I_e;
    //!  membrane time constant
    double tau_m;
    //!  synaptic time constant
    double tau_syn;
    //!  membrane capacitance
    double C_m;
    //!  threshold potential
    double V_theta;
    //!  mean of the noise current
    double mean_noise;
    //!  standard deviation of the noise current
    double sigma_noise;
    //!  time constant of the noise process
    double tau_noise;

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
    double V_m;
    double I_noise;
    double psc_kernel__X__spikes;

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
    double A_noise;
    double __h;
    double __P__V_m__V_m;
    double __P__V_m__psc_kernel__X__spikes;
    double __P__psc_kernel__X__spikes__psc_kernel__X__spikes;
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
    Buffers_(iaf_psc_exp_nestml &);
    Buffers_(const Buffers_ &, iaf_psc_exp_nestml &);

    /**
     * Logger for all analog data
    **/
    nest::UniversalDataLogger<iaf_psc_exp_nestml> logger_;

    // -----------------------------------------------------------------------
    //   Buffers and sums of incoming spikes/currents per timestep
    // -----------------------------------------------------------------------
    // Buffer containing the incoming spikes
    

inline std::vector< nest::RingBuffer >& get_spike_inputs_()
{
    return spike_inputs_;
}
std::vector< nest::RingBuffer > spike_inputs_;

    // Buffer containing the sum of all the incoming spikes
    

inline std::vector< double >& get_spike_inputs_grid_sum_()
{
    return spike_inputs_grid_sum_;
}
std::vector< double > spike_inputs_grid_sum_;
  };

  // -------------------------------------------------------------------------
  //   Getters/setters for inline expressions
  // -------------------------------------------------------------------------
  

  // -------------------------------------------------------------------------
  //   Getters/setters for input buffers
  // -------------------------------------------------------------------------

  // Buffer containing the incoming spikes
  

inline std::vector< nest::RingBuffer >& get_spike_inputs_()
{
    return B_.get_spike_inputs_();
}

  

inline std::vector< double >& get_spike_inputs_grid_sum_()
{
    return B_.get_spike_inputs_grid_sum_();
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
  static nest::RecordablesMap<iaf_psc_exp_nestml> recordablesMap_;
  nest::normal_distribution normal_dev_; //!< random deviate generator

}; /* neuron iaf_psc_exp_nestml */

inline nest_port_t iaf_psc_exp_nestml::send_test_event(nest::Node& target, nest_rport_t receptor_type, nest::synindex, bool)
{
  // You should usually not change the code in this function.
  // It confirms that the target of connection @c c accepts @c nest::SpikeEvent on
  // the given @c receptor_type.
  nest::SpikeEvent e;
  e.set_sender(*this);
  return target.handles_test_event(e, receptor_type);
}

inline nest_port_t iaf_psc_exp_nestml::handles_test_event(nest::SpikeEvent&, nest_port_t receptor_type)
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

inline nest_port_t iaf_psc_exp_nestml::handles_test_event(nest::DataLoggingRequest& dlr, nest_port_t receptor_type)
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

inline void iaf_psc_exp_nestml::get_status(DictionaryDatum &__d) const
{
  // parameters
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_E_L, get_E_L());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_I_e, get_I_e());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_tau_m, get_tau_m());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_tau_syn, get_tau_syn());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_C_m, get_C_m());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_V_theta, get_V_theta());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_mean_noise, get_mean_noise());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_sigma_noise, get_sigma_noise());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_tau_noise, get_tau_noise());

  // initial values for state variables in ODE or kernel
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_V_m, get_V_m());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_I_noise, get_I_noise());
  def<double>(__d, nest::iaf_psc_exp_nestml_names::_psc_kernel__X__spikes, get_psc_kernel__X__spikes());

  StructuralPlasticityNode::get_status( __d );

  (*__d)[nest::names::recordables] = recordablesMap_.get_list();
}

inline void iaf_psc_exp_nestml::set_status(const DictionaryDatum &__d)
{
  // parameters
  double tmp_E_L = get_E_L();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_E_L, tmp_E_L, this);
  double tmp_I_e = get_I_e();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_I_e, tmp_I_e, this);
  double tmp_tau_m = get_tau_m();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_tau_m, tmp_tau_m, this);
  double tmp_tau_syn = get_tau_syn();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_tau_syn, tmp_tau_syn, this);
  double tmp_C_m = get_C_m();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_C_m, tmp_C_m, this);
  double tmp_V_theta = get_V_theta();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_V_theta, tmp_V_theta, this);
  double tmp_mean_noise = get_mean_noise();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_mean_noise, tmp_mean_noise, this);
  double tmp_sigma_noise = get_sigma_noise();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_sigma_noise, tmp_sigma_noise, this);
  double tmp_tau_noise = get_tau_noise();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_tau_noise, tmp_tau_noise, this);

  // initial values for state variables in ODE or kernel
  double tmp_V_m = get_V_m();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_V_m, tmp_V_m, this);
  double tmp_I_noise = get_I_noise();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_I_noise, tmp_I_noise, this);
  double tmp_psc_kernel__X__spikes = get_psc_kernel__X__spikes();
  nest::updateValueParam<double>(__d, nest::iaf_psc_exp_nestml_names::_psc_kernel__X__spikes, tmp_psc_kernel__X__spikes, this);

  // We now know that (ptmp, stmp) are consistent. We do not
  // write them back to (P_, S_) before we are also sure that
  // the properties to be set in the parent class are internally
  // consistent.
  StructuralPlasticityNode::set_status(__d);

  // if we get here, temporaries contain consistent set of properties
  set_E_L(tmp_E_L);
  set_I_e(tmp_I_e);
  set_tau_m(tmp_tau_m);
  set_tau_syn(tmp_tau_syn);
  set_C_m(tmp_C_m);
  set_V_theta(tmp_V_theta);
  set_mean_noise(tmp_mean_noise);
  set_sigma_noise(tmp_sigma_noise);
  set_tau_noise(tmp_tau_noise);
  set_V_m(tmp_V_m);
  set_I_noise(tmp_I_noise);
  set_psc_kernel__X__spikes(tmp_psc_kernel__X__spikes);





  // recompute internal variables in case they are dependent on parameters or state that might have been updated in this call to set_status()
  recompute_internal_variables();
};



#endif /* #ifndef IAF_PSC_EXP_NESTML */
