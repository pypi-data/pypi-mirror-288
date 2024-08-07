
/**
 *  inhomogeneous_poisson_neuron_nestml.h
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
 *  Generated from NESTML at time: 2024-04-23 11:56:24.526802
**/
#ifndef INHOMOGENEOUS_POISSON_NEURON_NESTML
#define INHOMOGENEOUS_POISSON_NEURON_NESTML

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
namespace inhomogeneous_poisson_neuron_nestml_names
{
    const Name _idx( "idx" );
    const Name _dt_next_spike( "dt_next_spike" );
    const Name _t_last_spike( "t_last_spike" );
    const Name _N( "N" );
    const Name _rate_times( "rate_times" );
    const Name _rate_values( "rate_values" );
}
}




#include "nest_time.h"
  typedef size_t nest_port_t;
  typedef size_t nest_rport_t;

/* BeginDocumentation
  Name: inhomogeneous_poisson_neuron_nestml

  Description:

    """
  inhomogeneous_poisson - Inhomogeneous Poisson process model##########################################################

  Description
  +++++++++++

  Inhomogeneous Poisson process model.

  The rate of the model is piecewise constant and is defined by an array containing desired rates (in units of 1/s) and an array of equal length containing the corresponding times (in units of ms). Please see the documentation for the NEST built-in inhomogeneous_poisson_generator for more details [2].


  See also
  ++++++++

  See the inhomogeneous Poisson generator NESTML tutorial for a usage example.


  References
  ++++++++++

  [1] Wikipedia contributors. 'Poisson Point Process.' Wikipedia, The Free Encyclopedia. Accessed on February 23, 2024. https://en.wikipedia.org/wiki/Poisson_point_process.

  [2] https://nest-simulator.readthedocs.io/en/stable/models/inhomogeneous_poisson_generator.html
  """


  Parameters:
  The following parameters can be set in the status dictionary.


  Dynamic state variables:


  Sends: nest::SpikeEvent

  Receives:  DataLoggingRequest
*/

// Register the neuron model
void register_inhomogeneous_poisson_neuron_nestml( const std::string& name );

class inhomogeneous_poisson_neuron_nestml : public nest::StructuralPlasticityNode
{
public:
  /**
   * The constructor is only used to create the model prototype in the model manager.
  **/
  inhomogeneous_poisson_neuron_nestml();

  /**
   * The copy constructor is used to create model copies and instances of the model.
   * @node The copy constructor needs to initialize the parameters and the state.
   *       Initialization of buffers and interal variables is deferred to
   *       @c init_buffers_() and @c pre_run_hook() (or calibrate() in NEST 3.3 and older).
  **/
  inhomogeneous_poisson_neuron_nestml(const inhomogeneous_poisson_neuron_nestml &);

  /**
   * Destructor.
  **/
  ~inhomogeneous_poisson_neuron_nestml() override;

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



  void handle(nest::DataLoggingRequest &) override;//! allow recording with multimeter
  nest_port_t handles_test_event(nest::DataLoggingRequest&, nest_port_t) override;

  // -------------------------------------------------------------------------
  //   Functions for getting/setting parameters and state values.
  // -------------------------------------------------------------------------

  void get_status(DictionaryDatum &) const override;
  void set_status(const DictionaryDatum &) override;


  // -------------------------------------------------------------------------
  //   Getters/setters for state block
  // -------------------------------------------------------------------------

  inline long get_idx() const
  {
    return S_.idx;
  }

  inline void set_idx(const long __v)
  {
    S_.idx = __v;
  }

  inline double get_dt_next_spike() const
  {
    return S_.dt_next_spike;
  }

  inline void set_dt_next_spike(const double __v)
  {
    S_.dt_next_spike = __v;
  }

  inline double get_t_last_spike() const
  {
    return S_.t_last_spike;
  }

  inline void set_t_last_spike(const double __v)
  {
    S_.t_last_spike = __v;
  }


  // -------------------------------------------------------------------------
  //   Getters/setters for parameters
  // -------------------------------------------------------------------------

  inline long get_N() const
  {
    return P_.N;
  }

  inline void set_N(const long __v)
  {
    P_.N = __v;
  }

  inline std::vector< double >  get_rate_times() const
  {
    return P_.rate_times;
  }

  inline void set_rate_times(const std::vector< double >  __v)
  {
    P_.rate_times = __v;
  }

  inline std::vector< double >  get_rate_values() const
  {
    return P_.rate_values;
  }

  inline void set_rate_values(const std::vector< double >  __v)
  {
    P_.rate_values = __v;
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


  // -------------------------------------------------------------------------
  //   Methods corresponding to event handlers
  // -------------------------------------------------------------------------

  

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
    MAX_SPIKE_RECEPTOR = 0
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
  friend class nest::RecordablesMap<inhomogeneous_poisson_neuron_nestml>;
  friend class nest::UniversalDataLogger<inhomogeneous_poisson_neuron_nestml>;

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
    long N;
    std::vector< double >  rate_times;
    std::vector< double >  rate_values;

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
    long idx;
    double dt_next_spike;
    double t_last_spike;

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
    Buffers_(inhomogeneous_poisson_neuron_nestml &);
    Buffers_(const Buffers_ &, inhomogeneous_poisson_neuron_nestml &);

    /**
     * Logger for all analog data
    **/
    nest::UniversalDataLogger<inhomogeneous_poisson_neuron_nestml> logger_;

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
  static nest::RecordablesMap<inhomogeneous_poisson_neuron_nestml> recordablesMap_;
  nest::normal_distribution normal_dev_; //!< random deviate generator
  nest::poisson_distribution poisson_dev_; //!< random deviate generator

}; /* neuron inhomogeneous_poisson_neuron_nestml */

inline nest_port_t inhomogeneous_poisson_neuron_nestml::send_test_event(nest::Node& target, nest_rport_t receptor_type, nest::synindex, bool)
{
  // You should usually not change the code in this function.
  // It confirms that the target of connection @c c accepts @c nest::SpikeEvent on
  // the given @c receptor_type.
  nest::SpikeEvent e;
  e.set_sender(*this);
  return target.handles_test_event(e, receptor_type);
}

inline nest_port_t inhomogeneous_poisson_neuron_nestml::handles_test_event(nest::DataLoggingRequest& dlr, nest_port_t receptor_type)
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

inline void inhomogeneous_poisson_neuron_nestml::get_status(DictionaryDatum &__d) const
{
  // parameters
  def<long>(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_N, get_N());
  def<std::vector< double > >(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_rate_times, get_rate_times());
  def<std::vector< double > >(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_rate_values, get_rate_values());

  // initial values for state variables in ODE or kernel
  def<long>(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_idx, get_idx());
  def<double>(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_dt_next_spike, get_dt_next_spike());
  def<double>(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_t_last_spike, get_t_last_spike());

  StructuralPlasticityNode::get_status( __d );

  (*__d)[nest::names::recordables] = recordablesMap_.get_list();
}

inline void inhomogeneous_poisson_neuron_nestml::set_status(const DictionaryDatum &__d)
{
  // parameters
  long tmp_N = get_N();
  nest::updateValueParam<long>(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_N, tmp_N, this);
  // Resize vectors
  if (tmp_N != get_N())
  {
    std::vector< double >  _tmp_rate_times = get_rate_times();
    _tmp_rate_times.resize(tmp_N, 0.);
    set_rate_times(_tmp_rate_times);
    std::vector< double >  _tmp_rate_values = get_rate_values();
    _tmp_rate_values.resize(tmp_N, 0.);
    set_rate_values(_tmp_rate_values);
  }
  std::vector< double >  tmp_rate_times = get_rate_times();
  updateValue<std::vector< double > >(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_rate_times, tmp_rate_times);
  // Resize vectors
  if (tmp_rate_times != get_rate_times())
  {
  }
   
  // Check if the new vector size matches its original size
  if ( tmp_rate_times.size() != tmp_N )
  {
    std::stringstream msg;
    msg << "The vector \"rate_times\" does not match its size: " << tmp_N;
    throw nest::BadProperty(msg.str());
  }
  std::vector< double >  tmp_rate_values = get_rate_values();
  updateValue<std::vector< double > >(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_rate_values, tmp_rate_values);
  // Resize vectors
  if (tmp_rate_values != get_rate_values())
  {
  }
   
  // Check if the new vector size matches its original size
  if ( tmp_rate_values.size() != tmp_N )
  {
    std::stringstream msg;
    msg << "The vector \"rate_values\" does not match its size: " << tmp_N;
    throw nest::BadProperty(msg.str());
  }

  // initial values for state variables in ODE or kernel
  long tmp_idx = get_idx();
  nest::updateValueParam<long>(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_idx, tmp_idx, this);
  double tmp_dt_next_spike = get_dt_next_spike();
  nest::updateValueParam<double>(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_dt_next_spike, tmp_dt_next_spike, this);
  double tmp_t_last_spike = get_t_last_spike();
  nest::updateValueParam<double>(__d, nest::inhomogeneous_poisson_neuron_nestml_names::_t_last_spike, tmp_t_last_spike, this);

  // We now know that (ptmp, stmp) are consistent. We do not
  // write them back to (P_, S_) before we are also sure that
  // the properties to be set in the parent class are internally
  // consistent.
  StructuralPlasticityNode::set_status(__d);

  // if we get here, temporaries contain consistent set of properties
  set_N(tmp_N);
  set_rate_times(tmp_rate_times);
  set_rate_values(tmp_rate_values);
  set_idx(tmp_idx);
  set_dt_next_spike(tmp_dt_next_spike);
  set_t_last_spike(tmp_t_last_spike);





  // recompute internal variables in case they are dependent on parameters or state that might have been updated in this call to set_status()
  recompute_internal_variables();
};



#endif /* #ifndef INHOMOGENEOUS_POISSON_NEURON_NESTML */
