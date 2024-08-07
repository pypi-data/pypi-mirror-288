/**
 *  syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml.h
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
 *  Generated from NESTML at time: 2024-02-26 10:01:24.137162
**/

#ifndef SYN_GL_CA5BC3B424B39F483C8FC6AA7320AB1D07_NESTML__WITH_GL_CA5BC3B424B39F483C8FC6AA7320AB1D07_NESTML_H
#define SYN_GL_CA5BC3B424B39F483C8FC6AA7320AB1D07_NESTML__WITH_GL_CA5BC3B424B39F483C8FC6AA7320AB1D07_NESTML_H

// C++ includes:
#include <cmath>

// Includes from nestkernel:
#include "common_synapse_properties.h"
#include "connection.h"
#include "connector_model.h"
#include "event.h"


// Includes from sli:
#include "dictdatum.h"
#include "dictutils.h"

/** @BeginDocumentation

**/

//#define DEBUG

namespace nest
{

namespace syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml_names
{
    const Name _R_pre( "R_pre" );
    const Name _the_delay( "the_delay" );
    const Name _lmbda( "lmbda" );
}

class syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestmlCommonSynapseProperties : public CommonSynapseProperties {
public:

    syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestmlCommonSynapseProperties()
    : CommonSynapseProperties()
    {
    }

    /**
     * Get all properties and put them into a dictionary.
     */
    void get_status( DictionaryDatum& d ) const
    {
        CommonSynapseProperties::get_status( d );
    }


    /**
     * Set properties from the values given in dictionary.
     */
    void set_status( const DictionaryDatum& d, ConnectorModel& cm )
    {
      CommonSynapseProperties::set_status( d, cm );
    }

    // N.B.: we define all parameters as public for easy reference conversion later on.
    // This may or may not benefit performance (TODO: compare with inline getters/setters)
};


template < typename targetidentifierT >
class syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml : public Connection< targetidentifierT >
{
  typedef gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml post_neuron_t;


private:
  double t_lastspike_;

  /**
   * Dynamic state of the synapse.
   *
   * These are the state variables that are advanced in time by calls to
   * send(). In many models, some or all of them can be set by the user
   * through ``SetStatus()``.
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
  struct State_{    
    double R_pre;

    State_() {};
  };

  /**
   * Free parameters of the synapse.
   *


   *
   * These are the parameters that can be set by the user through @c SetStatus.
   * Parameters do not change during calls to ``send()`` and are not reset by
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
  */
  struct Parameters_{    
    //!  !!! cannot have a variable called "delay"
    double the_delay;
    //!  residual calcium decay rate
    double lmbda;



    /** Initialize parameters to their default values. */
    Parameters_() {};
  };

  /**
   * Internal variables of the synapse.
   *
   *
   * These variables must be initialized by recompute_internal_variables().
  **/
  struct Variables_
  {    
    double __h;
  };

  Parameters_ P_;  //!< Free parameters.
  State_      S_;  //!< Dynamic state.
  Variables_  V_;  //!< Internal Variables
  // -------------------------------------------------------------------------
  //   Getters/setters for state block
  // -------------------------------------------------------------------------

  inline double get_R_pre() const
  {
    return S_.R_pre;
  }

  inline void set_R_pre(const double __v)
  {
    S_.R_pre = __v;
  }


  // -------------------------------------------------------------------------
  //   Getters/setters for parameters
  // -------------------------------------------------------------------------

  inline double get_the_delay() const
  {
    return P_.the_delay;
  }

  inline void set_the_delay(const double __v)
  {
    P_.the_delay = __v;
  }inline double get_lmbda() const
  {
    return P_.lmbda;
  }

  inline void set_lmbda(const double __v)
  {
    P_.lmbda = __v;
  }

  // -------------------------------------------------------------------------
  //   Getters/setters for inline expressions
  // -------------------------------------------------------------------------

  

  // -------------------------------------------------------------------------
  //   Function declarations
  // -------------------------------------------------------------------------



  /**
   * Update internal state (``S_``) of the synapse according to the dynamical equations defined in the model and the statements in the ``update`` block.
  **/
  inline void
  update_internal_state_(double t_start, double timestep, const syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestmlCommonSynapseProperties& cp);

  void recompute_internal_variables();

public:
  // this line determines which common properties to use
  typedef syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestmlCommonSynapseProperties CommonPropertiesType;

  typedef Connection< targetidentifierT > ConnectionBase;
  static constexpr ConnectionModelProperties properties = ConnectionModelProperties::HAS_DELAY
    | ConnectionModelProperties::IS_PRIMARY | ConnectionModelProperties::SUPPORTS_HPC
    | ConnectionModelProperties::SUPPORTS_LBL;

  /**
  * Default constructor.
  *
  * Sets default values for all parameters (skipping common properties).
  *
  * Needed by GenericConnectorModel.
  */
  syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml();

  /**
  * Copy constructor from a property object.
  *
  * Sets default values for all parameters (skipping common properties).
  *
  * Needs to be defined properly in order for GenericConnector to work.
  */
  syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml( const syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml& rhs );

  // Explicitly declare all methods inherited from the dependent base
  // ConnectionBase. This avoids explicit name prefixes in all places these
  // functions are used. Since ConnectionBase depends on the template parameter,
  // they are not automatically found in the base class.
  using ConnectionBase::get_delay_steps;
  using ConnectionBase::set_delay_steps;
  using ConnectionBase::get_delay;
  using ConnectionBase::set_delay;
  using ConnectionBase::get_rport;
  using ConnectionBase::get_target;


  class ConnTestDummyNode : public ConnTestDummyNodeBase
  {
  public:
    // Ensure proper overriding of overloaded virtual functions.
    // Return values from functions are ignored.
    using ConnTestDummyNodeBase::handles_test_event;
    size_t
    handles_test_event( SpikeEvent&, size_t ) override
    {
      return invalid_port;
    }
    size_t
    handles_test_event( RateEvent&, size_t ) override
    {
      return invalid_port;    }
    size_t
    handles_test_event( DataLoggingRequest&, size_t ) override
    {
      return invalid_port;    }
    size_t
    handles_test_event( CurrentEvent&, size_t ) override
    {
      return invalid_port;    }
    size_t
    handles_test_event( ConductanceEvent&, size_t ) override
    {
      return invalid_port;    }
    size_t
    handles_test_event( DoubleDataEvent&, size_t ) override
    {
      return invalid_port;    }
    size_t
    handles_test_event( DSSpikeEvent&, size_t ) override
    {
      return invalid_port;    }
    size_t
    handles_test_event( DSCurrentEvent&, size_t ) override
    {
      return invalid_port;    }
  };

  /**
   *  special case for weights in NEST: only in case a NESTML state variable was decorated by @nest::weight
  **/
  inline void set_weight(double w)
  {

    // no variable was decorated by @nest::weight, so no "weight" defined from the NEST perspective
    assert(0);
  }
  void
  check_connection( Node& s,
    Node& t,
    size_t receptor_type,
    const CommonPropertiesType& cp )
  {
    ConnTestDummyNode dummy_target;
    ConnectionBase::check_connection_( dummy_target, s, t, receptor_type );
    try {
      dynamic_cast<gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml&>(t);
    }
    catch (std::bad_cast &exp) {
      std::cout << "wrong type of neuron connected! Synapse 'syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml' will only work with neuron 'gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml'.\n";
      exit(1);
    }

    t.register_stdp_connection( t_lastspike_ - get_delay(), get_delay() );
  }
  void
  send( Event& e, const size_t tid, const syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestmlCommonSynapseProperties& cp )
  {
    const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

    auto get_thread = [tid]()
    {
        return tid;
    };

    const double __t_spike = e.get_stamp().get_ms();
#ifdef DEBUG
    std::cout << "syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml::send(): handling pre spike at t = " << __t_spike << std::endl;
#endif
    // use accessor functions (inherited from Connection< >) to obtain delay and target
    gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml* __target = static_cast<gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml*>(get_target(tid));
    assert(__target);
    const double __dendritic_delay = get_delay();
    const bool pre_before_post_update = 0;
    bool pre_before_post_flag = false;

    if (t_lastspike_ < 0.)
    {
        // this is the first presynaptic spike to be processed
        t_lastspike_ = 0.;
    }
    double timestep = 0;

    {
      // get spike history in relevant range (t1, t2] from post-synaptic neuron
      std::deque< histentry__gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml >::iterator start;
      std::deque< histentry__gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml >::iterator finish;
      // For a new synapse, t_lastspike_ contains the point in time of the last
      // spike. So we initially read the
      // history(t_last_spike - dendritic_delay, ..., T_spike-dendritic_delay]
      // which increases the access counter for these entries.
      // At registration, all entries' access counters of
      // history[0, ..., t_last_spike - dendritic_delay] have been
      // incremented by Archiving_Node::register_stdp_connection(). See bug #218 for
      // details.
      __target->get_history__( t_lastspike_ - __dendritic_delay,
        __t_spike - __dendritic_delay,
        &start,
        &finish );
      // facilitation due to post-synaptic spikes since last pre-synaptic spike
      while ( start != finish )
      {
        const double minus_dt = t_lastspike_ - ( start->t_ + __dendritic_delay );
        // get_history() should make sure that
        // start->t_ > t_lastspike_ - dendritic_delay, i.e. minus_dt < 0
        assert( minus_dt < -kernel().connection_manager.get_stdp_eps() );

        if (pre_before_post_update and start->t_ == __t_spike - __dendritic_delay)
        {
          pre_before_post_flag = true;
          break;  // this would in any case have been the last post spike to be processed
        }

#ifdef DEBUG
        std::cout << "\tprocessing post spike at t = " << start->t_ << std::endl;
#endif

        /**
         * update synapse internal state from `t_lastspike_` to `start->t_`
        **/

        update_internal_state_(t_lastspike_, (start->t_ + __dendritic_delay) - t_lastspike_, cp);

        timestep += (start->t_ + __dendritic_delay) - t_lastspike_;

        const double _tr_t = start->t_;
        auto get_t = [_tr_t](){ return _tr_t; };   // do not remove, this is in case the predefined time variable ``t`` is used in the NESTML model      

        /**
         * internal state has now been fully updated to `start->t_ + __dendritic_delay`
        **/

        t_lastspike_ = start->t_ + __dendritic_delay;
        ++start;
      }
    }

    /**
     * update synapse internal state from `t_lastspike_` to `__t_spike`
    **/

    update_internal_state_(t_lastspike_, __t_spike - t_lastspike_, cp);

    const double _tr_t = __t_spike - __dendritic_delay;

    {
        auto get_t = [__t_spike](){ return __t_spike; };    // do not remove, this is in case the predefined time variable ``t`` is used in the NESTML model        
        /**
         *  NESTML generated onReceive code block for presynaptic port "incoming_spikes" begins here!
        **/
        S_.R_pre += 1;

                set_delay( P_.the_delay );
                const long __delay_steps = nest::Time::delay_ms_to_steps( get_delay() );
                set_delay_steps(__delay_steps);
                e.set_receiver( *__target );
          e.set_weight( S_.R_pre - 1 );
          // use accessor functions (inherited from Connection< >) to obtain delay in steps and rport
          e.set_delay_steps( get_delay_steps() );
          e.set_rport( get_rport() );
        e();
        ;
    }

    /**
     *  update all convolutions with pre spikes
    **/



    /**
     *  in case pre and post spike time coincide and pre update takes priority
    **/

    if (pre_before_post_flag)
    {
        auto get_t = [__t_spike](){ return __t_spike; };    // do not remove, this is in case the predefined time variable ``t`` is used in the NESTML model      
    }

    /**
     *  synapse internal state has now been fully updated to `__t_spike`
    **/

    t_lastspike_ = __t_spike;
  }

  void get_status( DictionaryDatum& d ) const;

  void set_status( const DictionaryDatum& d, ConnectorModel& cm );
};
template < typename targetidentifierT >
constexpr ConnectionModelProperties syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml< targetidentifierT >::properties;


template < typename targetidentifierT >
void
syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml< targetidentifierT >::get_status( DictionaryDatum& __d ) const
{
  ConnectionBase::get_status( __d );
  def< long >( __d, names::size_of, sizeof( *this ) );

  // parameters
  def< double >( __d, names::delay, P_.the_delay );  
  def<double>(__d, nest::syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml_names::_lmbda, get_lmbda());

  // initial values for state variables in ODE or kernel  
  def<double>(__d, nest::syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml_names::_R_pre, get_R_pre());
}

template < typename targetidentifierT >
void
syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml< targetidentifierT >::set_status( const DictionaryDatum& __d,
  ConnectorModel& cm )
{
  // parameters  
  double tmp_the_delay = get_the_delay();
  updateValue<double>(__d, nest::syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml_names::_the_delay, tmp_the_delay);  
  double tmp_lmbda = get_lmbda();
  updateValue<double>(__d, nest::syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml_names::_lmbda, tmp_lmbda);

  // initial values for state variables in ODE or kernel  
  double tmp_R_pre = get_R_pre();
  updateValue<double>(__d, nest::syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml_names::_R_pre, tmp_R_pre);


  // We now know that (ptmp, stmp) are consistent. We do not
  // write them back to (P_, S_) before we are also sure that
  // the properties to be set in the parent class are internally
  // consistent.
  ConnectionBase::set_status( __d, cm );

  // if we get here, temporaries contain consistent set of properties

  // set parameters  
  set_the_delay(tmp_the_delay);  
  set_lmbda(tmp_lmbda);

  // set state  
  set_R_pre(tmp_R_pre);

  // check invariants



  // special treatment of NEST delay
  set_delay(
get_the_delay());

  // recompute internal variables in case they are dependent on parameters or state that might have been updated in this call to set_status()
  recompute_internal_variables();
}

/**
 * NESTML internals block symbols initialisation
**/
template < typename targetidentifierT >
void syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml< targetidentifierT >::recompute_internal_variables()
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function


}

/**
 * constructor
**/
template < typename targetidentifierT >
syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml< targetidentifierT >::syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml() : ConnectionBase()
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  

  P_.the_delay = 1; // as ms
  

  P_.lmbda = 2.1555489309487914; // as real

  V_.__h = nest::Time::get_resolution().get_ms();
  recompute_internal_variables();

  // initial values for state variables in ODE or kernel
  

  S_.R_pre = 0.0; // as real

  t_lastspike_ = 0.;
}

/**
 * copy constructor
**/
template < typename targetidentifierT >
syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml< targetidentifierT >::syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml( const syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml< targetidentifierT >& rhs )
: ConnectionBase( rhs )
{
    P_.the_delay = rhs.P_.the_delay;
    P_.lmbda = rhs.P_.lmbda;

  // state variables in ODE or kernel
    S_.R_pre = rhs.S_.R_pre;

    //weight_ = get_named_parameter<double>(names::weight);
    //set_weight( *rhs.weight_ );
    t_lastspike_ = rhs.t_lastspike_;

    // special treatment of NEST delay
    set_delay(rhs.get_delay());
}

template < typename targetidentifierT >
inline void
syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml< targetidentifierT >::update_internal_state_(double t_start, double timestep, const syn_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestml__with_gl_ca5bc3b424b39f483c8fc6aa7320ab1d07_nestmlCommonSynapseProperties& cp)
{
  if (timestep < 1E-12)
  {
#ifdef DEBUG
    std::cout << "\tupdate_internal_state_() called with dt < 1E-12; skipping update\n" ;
#endif
    return;
  }

  const double __resolution = timestep;  // do not remove, this is necessary for the resolution() function
  auto get_t = [t_start](){ return t_start; };   // do not remove, this is in case the predefined time variable ``t`` is used in the NESTML model

#ifdef DEBUG
  std::cout<< "\tUpdating internal state: t_start = " << t_start << ", dt = " << timestep << "\n";
#endif
  const double old___h = V_.__h;
  V_.__h = timestep;
  recompute_internal_variables();  
  /* replace analytically solvable variables with precisely integrated values  */
    V_.__h = old___h;
    recompute_internal_variables();  // XXX: can be skipped?

    // NESTML generated code for the update block:
  S_.R_pre *= std::exp((-P_.lmbda) * 0.001 * __resolution);
}

} // namespace

#endif /* #ifndef SYN_GL_CA5BC3B424B39F483C8FC6AA7320AB1D07_NESTML__WITH_GL_CA5BC3B424B39F483C8FC6AA7320AB1D07_NESTML_H */