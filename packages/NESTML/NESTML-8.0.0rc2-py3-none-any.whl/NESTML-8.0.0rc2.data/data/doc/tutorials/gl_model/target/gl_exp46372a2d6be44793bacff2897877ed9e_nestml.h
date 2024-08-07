
/**
 *  gl_exp46372a2d6be44793bacff2897877ed9e_nestml.h
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
 *  Generated from NESTML at time: 2024-02-26 09:15:22.284658
**/
#ifndef GL_EXP46372A2D6BE44793BACFF2897877ED9E_NESTML
#define GL_EXP46372A2D6BE44793BACFF2897877ED9E_NESTML

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
namespace gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names
{
    const Name _refr_spikes_buffer( "refr_spikes_buffer" );
    const Name _refr_tick( "refr_tick" );
    const Name _V_m( "V_m" );
    const Name _tau_m( "tau_m" );
    const Name _C_m( "C_m" );
    const Name _t_ref( "t_ref" );
    const Name _tau_syn( "tau_syn" );
    const Name _V_r( "V_r" );
    const Name _V_reset( "V_reset" );
    const Name _b( "b" );
    const Name _a( "a" );
    const Name _V_b( "V_b" );
    const Name _with_refr_input( "with_refr_input" );
    const Name _reset_after_spike( "reset_after_spike" );
    const Name _I_e( "I_e" );
}
}




#include "nest_time.h"
  typedef size_t nest_port_t;
  typedef size_t nest_rport_t;

/* BeginDocumentation
  Name: gl_exp46372a2d6be44793bacff2897877ed9e_nestml

  Description:

    

  Parameters:
  The following parameters can be set in the status dictionary.
tau_m [ms]  Membrane time constant
C_m [pF]  Capacity of the membrane
t_ref [ms]  Duration of refractory period
tau_syn [ms]  Time constant of synaptic current
V_r [mV]  Resting membrane potential
V_reset [mV]  Reset potential of the membrane
b [real]  Parameter for the exponential curve
a [mV]  Parameter for the exponential curve
V_b [mV]  Membrane potential at which phi(V)=1/b
with_refr_input [boolean]  If true, do not discard input during refractory period.
I_e [pA]  constant external input current


  Dynamic state variables:
refr_tick [integer]  Counts number of tick during the refractory period
V_m [mV]  Membrane potential


  Sends: nest::SpikeEvent

  Receives: Spike, Current, DataLoggingRequest
*/
class gl_exp46372a2d6be44793bacff2897877ed9e_nestml : public nest::StructuralPlasticityNode
{
public:
  /**
   * The constructor is only used to create the model prototype in the model manager.
  **/
  gl_exp46372a2d6be44793bacff2897877ed9e_nestml();

  /**
   * The copy constructor is used to create model copies and instances of the model.
   * @node The copy constructor needs to initialize the parameters and the state.
   *       Initialization of buffers and interal variables is deferred to
   *       @c init_buffers_() and @c pre_run_hook() (or calibrate() in NEST 3.3 and older).
  **/
  gl_exp46372a2d6be44793bacff2897877ed9e_nestml(const gl_exp46372a2d6be44793bacff2897877ed9e_nestml &);

  /**
   * Destructor.
  **/
  ~gl_exp46372a2d6be44793bacff2897877ed9e_nestml() override;

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


  // -------------------------------------------------------------------------
  //   Getters/setters for state block
  // -------------------------------------------------------------------------

  inline double get_refr_spikes_buffer() const
  {
    return S_.refr_spikes_buffer;
  }

  inline void set_refr_spikes_buffer(const double __v)
  {
    S_.refr_spikes_buffer = __v;
  }

  inline long get_refr_tick() const
  {
    return S_.refr_tick;
  }

  inline void set_refr_tick(const long __v)
  {
    S_.refr_tick = __v;
  }

  inline double get_V_m() const
  {
    return S_.V_m;
  }

  inline void set_V_m(const double __v)
  {
    S_.V_m = __v;
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

  inline double get_t_ref() const
  {
    return P_.t_ref;
  }

  inline void set_t_ref(const double __v)
  {
    P_.t_ref = __v;
  }

  inline double get_tau_syn() const
  {
    return P_.tau_syn;
  }

  inline void set_tau_syn(const double __v)
  {
    P_.tau_syn = __v;
  }

  inline double get_V_r() const
  {
    return P_.V_r;
  }

  inline void set_V_r(const double __v)
  {
    P_.V_r = __v;
  }

  inline double get_V_reset() const
  {
    return P_.V_reset;
  }

  inline void set_V_reset(const double __v)
  {
    P_.V_reset = __v;
  }

  inline double get_b() const
  {
    return P_.b;
  }

  inline void set_b(const double __v)
  {
    P_.b = __v;
  }

  inline double get_a() const
  {
    return P_.a;
  }

  inline void set_a(const double __v)
  {
    P_.a = __v;
  }

  inline double get_V_b() const
  {
    return P_.V_b;
  }

  inline void set_V_b(const double __v)
  {
    P_.V_b = __v;
  }

  inline bool get_with_refr_input() const
  {
    return P_.with_refr_input;
  }

  inline void set_with_refr_input(const bool __v)
  {
    P_.with_refr_input = __v;
  }

  inline bool get_reset_after_spike() const
  {
    return P_.reset_after_spike;
  }

  inline void set_reset_after_spike(const bool __v)
  {
    P_.reset_after_spike = __v;
  }

  inline double get_I_e() const
  {
    return P_.I_e;
  }

  inline void set_I_e(const double __v)
  {
    P_.I_e = __v;
  }


  // -------------------------------------------------------------------------
  //   Getters/setters for internals
  // -------------------------------------------------------------------------

  inline long get_RefractoryCounts() const
  {
    return V_.RefractoryCounts;
  }

  inline void set_RefractoryCounts(const long __v)
  {
    V_.RefractoryCounts = __v;
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
  friend class nest::RecordablesMap<gl_exp46372a2d6be44793bacff2897877ed9e_nestml>;
  friend class nest::UniversalDataLogger<gl_exp46372a2d6be44793bacff2897877ed9e_nestml>;

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
    double t_ref;
    //!  Time constant of synaptic current
    double tau_syn;
    //!  Resting membrane potential
    double V_r;
    //!  Reset potential of the membrane
    double V_reset;
    //!  Parameter for the exponential curve
    double b;
    //!  Parameter for the exponential curve
    double a;
    //!  Membrane potential at which phi(V)=1/b
    double V_b;
    //!  If true, do not discard input during refractory period.
    bool with_refr_input;
    bool reset_after_spike;
    //!  constant external input current
    double I_e;

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
    double refr_spikes_buffer;
    //!  Counts number of tick during the refractory period
    long refr_tick;
    //!  Membrane potential
    double V_m;

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
    //!  refractory time in steps
    long RefractoryCounts;
    double __h;
    double __P__V_m__V_m;
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
    Buffers_(gl_exp46372a2d6be44793bacff2897877ed9e_nestml &);
    Buffers_(const Buffers_ &, gl_exp46372a2d6be44793bacff2897877ed9e_nestml &);

    /**
     * Logger for all analog data
    **/
    nest::UniversalDataLogger<gl_exp46372a2d6be44793bacff2897877ed9e_nestml> logger_;

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

  // Buffer containing the incoming spikes
  

inline std::vector< nest::RingBuffer >& get_spike_inputs_()
{
    return B_.get_spike_inputs_();
}

  

inline std::vector< double >& get_spike_inputs_grid_sum_()
{
    return B_.get_spike_inputs_grid_sum_();
}
  
inline nest::RingBuffer& get_I_stim() {
    return B_.get_I_stim();
}
  // -------------------------------------------------------------------------
  //   Function declarations
  // -------------------------------------------------------------------------



  //
  double phi ( double V_m) const;

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
  static nest::RecordablesMap<gl_exp46372a2d6be44793bacff2897877ed9e_nestml> recordablesMap_;

}; /* neuron gl_exp46372a2d6be44793bacff2897877ed9e_nestml */

inline nest_port_t gl_exp46372a2d6be44793bacff2897877ed9e_nestml::send_test_event(nest::Node& target, nest_rport_t receptor_type, nest::synindex, bool)
{
  // You should usually not change the code in this function.
  // It confirms that the target of connection @c c accepts @c nest::SpikeEvent on
  // the given @c receptor_type.
  nest::SpikeEvent e;
  e.set_sender(*this);
  return target.handles_test_event(e, receptor_type);
}

inline nest_port_t gl_exp46372a2d6be44793bacff2897877ed9e_nestml::handles_test_event(nest::SpikeEvent&, nest_port_t receptor_type)
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

inline nest_port_t gl_exp46372a2d6be44793bacff2897877ed9e_nestml::handles_test_event(nest::CurrentEvent&, nest_port_t receptor_type)
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

inline nest_port_t gl_exp46372a2d6be44793bacff2897877ed9e_nestml::handles_test_event(nest::DataLoggingRequest& dlr, nest_port_t receptor_type)
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

inline void gl_exp46372a2d6be44793bacff2897877ed9e_nestml::get_status(DictionaryDatum &__d) const
{
  // parameters
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_tau_m, get_tau_m());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_C_m, get_C_m());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_t_ref, get_t_ref());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_tau_syn, get_tau_syn());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_V_r, get_V_r());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_V_reset, get_V_reset());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_b, get_b());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_a, get_a());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_V_b, get_V_b());
  def<bool>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_with_refr_input, get_with_refr_input());
  def<bool>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_reset_after_spike, get_reset_after_spike());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_I_e, get_I_e());

  // initial values for state variables in ODE or kernel
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_refr_spikes_buffer, get_refr_spikes_buffer());
  def<long>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_refr_tick, get_refr_tick());
  def<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_V_m, get_V_m());

  StructuralPlasticityNode::get_status( __d );

  (*__d)[nest::names::recordables] = recordablesMap_.get_list();
}

inline void gl_exp46372a2d6be44793bacff2897877ed9e_nestml::set_status(const DictionaryDatum &__d)
{
  // parameters
  double tmp_tau_m = get_tau_m();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_tau_m, tmp_tau_m, this);
  double tmp_C_m = get_C_m();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_C_m, tmp_C_m, this);
  double tmp_t_ref = get_t_ref();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_t_ref, tmp_t_ref, this);
  double tmp_tau_syn = get_tau_syn();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_tau_syn, tmp_tau_syn, this);
  double tmp_V_r = get_V_r();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_V_r, tmp_V_r, this);
  double tmp_V_reset = get_V_reset();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_V_reset, tmp_V_reset, this);
  double tmp_b = get_b();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_b, tmp_b, this);
  double tmp_a = get_a();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_a, tmp_a, this);
  double tmp_V_b = get_V_b();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_V_b, tmp_V_b, this);
  bool tmp_with_refr_input = get_with_refr_input();
  nest::updateValueParam<bool>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_with_refr_input, tmp_with_refr_input, this);
  bool tmp_reset_after_spike = get_reset_after_spike();
  nest::updateValueParam<bool>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_reset_after_spike, tmp_reset_after_spike, this);
  double tmp_I_e = get_I_e();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_I_e, tmp_I_e, this);

  // initial values for state variables in ODE or kernel
  double tmp_refr_spikes_buffer = get_refr_spikes_buffer();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_refr_spikes_buffer, tmp_refr_spikes_buffer, this);
  long tmp_refr_tick = get_refr_tick();
  nest::updateValueParam<long>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_refr_tick, tmp_refr_tick, this);
  double tmp_V_m = get_V_m();
  nest::updateValueParam<double>(__d, nest::gl_exp46372a2d6be44793bacff2897877ed9e_nestml_names::_V_m, tmp_V_m, this);

  // We now know that (ptmp, stmp) are consistent. We do not
  // write them back to (P_, S_) before we are also sure that
  // the properties to be set in the parent class are internally
  // consistent.
  StructuralPlasticityNode::set_status(__d);

  // if we get here, temporaries contain consistent set of properties
  set_tau_m(tmp_tau_m);
  set_C_m(tmp_C_m);
  set_t_ref(tmp_t_ref);
  set_tau_syn(tmp_tau_syn);
  set_V_r(tmp_V_r);
  set_V_reset(tmp_V_reset);
  set_b(tmp_b);
  set_a(tmp_a);
  set_V_b(tmp_V_b);
  set_with_refr_input(tmp_with_refr_input);
  set_reset_after_spike(tmp_reset_after_spike);
  set_I_e(tmp_I_e);
  set_refr_spikes_buffer(tmp_refr_spikes_buffer);
  set_refr_tick(tmp_refr_tick);
  set_V_m(tmp_V_m);





  // recompute internal variables in case they are dependent on parameters or state that might have been updated in this call to set_status()
  recompute_internal_variables();
};



#endif /* #ifndef GL_EXP46372A2D6BE44793BACFF2897877ED9E_NESTML */
