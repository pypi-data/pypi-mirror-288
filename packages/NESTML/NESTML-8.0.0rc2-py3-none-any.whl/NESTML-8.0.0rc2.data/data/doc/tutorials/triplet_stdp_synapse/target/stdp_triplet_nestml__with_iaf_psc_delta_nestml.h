/**
 *  stdp_triplet_nestml__with_iaf_psc_delta_nestml.h
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
 *  Generated from NESTML at time: 2024-04-04 09:02:05.863377
**/

#ifndef STDP_TRIPLET_NESTML__WITH_IAF_PSC_DELTA_NESTML_H
#define STDP_TRIPLET_NESTML__WITH_IAF_PSC_DELTA_NESTML_H

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
// Register the synapse model
void register_stdp_triplet_nestml__with_iaf_psc_delta_nestml( const std::string& name );

namespace stdp_triplet_nestml__with_iaf_psc_delta_nestml_names
{
    const Name _w( "w" );
    const Name _tr_r1( "tr_r1" );
    const Name _tr_r2( "tr_r2" );
    const Name _d( "d" );
    const Name _tau_plus( "tau_plus" );
    const Name _tau_x( "tau_x" );
    const Name _tau_minus( "tau_minus" );
    const Name _tau_y( "tau_y" );
    const Name _A2_plus( "A2_plus" );
    const Name _A3_plus( "A3_plus" );
    const Name _A2_minus( "A2_minus" );
    const Name _A3_minus( "A3_minus" );
    const Name _Wmax( "Wmax" );
    const Name _Wmin( "Wmin" );
}

class stdp_triplet_nestml__with_iaf_psc_delta_nestmlCommonSynapseProperties : public CommonSynapseProperties {
public:

    stdp_triplet_nestml__with_iaf_psc_delta_nestmlCommonSynapseProperties()
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
class stdp_triplet_nestml__with_iaf_psc_delta_nestml : public Connection< targetidentifierT >
{
  typedef iaf_psc_delta_nestml__with_stdp_triplet_nestml post_neuron_t;


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
    double w;
    double tr_r1;
    double tr_r2;

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
    double d;
    //!  time constant for tr_r1
    double tau_plus;
    //!  time constant for tr_r2
    double tau_x;
    //!  time constant for tr_o1
    double tau_minus;
    //!  time constant for tr_o2
    double tau_y;
    double A2_plus;
    double A3_plus;
    double A2_minus;
    double A3_minus;
    double Wmax;
    double Wmin;



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
    double __P__tr_r1__tr_r1;    
    double __P__tr_r2__tr_r2;
  };

  Parameters_ P_;  //!< Free parameters.
  State_      S_;  //!< Dynamic state.
  Variables_  V_;  //!< Internal Variables
  // -------------------------------------------------------------------------
  //   Getters/setters for state block
  // -------------------------------------------------------------------------

  inline double get_w() const
  {
    return S_.w;
  }

  inline void set_w(const double __v)
  {
    S_.w = __v;
  }

  inline double get_tr_r1() const
  {
    return S_.tr_r1;
  }

  inline void set_tr_r1(const double __v)
  {
    S_.tr_r1 = __v;
  }

  inline double get_tr_r2() const
  {
    return S_.tr_r2;
  }

  inline void set_tr_r2(const double __v)
  {
    S_.tr_r2 = __v;
  }


  // -------------------------------------------------------------------------
  //   Getters/setters for parameters
  // -------------------------------------------------------------------------

  inline double get_d() const
  {
    return P_.d;
  }

  inline void set_d(const double __v)
  {
    P_.d = __v;
  }inline double get_tau_plus() const
  {
    return P_.tau_plus;
  }

  inline void set_tau_plus(const double __v)
  {
    P_.tau_plus = __v;
  }inline double get_tau_x() const
  {
    return P_.tau_x;
  }

  inline void set_tau_x(const double __v)
  {
    P_.tau_x = __v;
  }inline double get_tau_minus() const
  {
    return P_.tau_minus;
  }

  inline void set_tau_minus(const double __v)
  {
    P_.tau_minus = __v;
  }inline double get_tau_y() const
  {
    return P_.tau_y;
  }

  inline void set_tau_y(const double __v)
  {
    P_.tau_y = __v;
  }inline double get_A2_plus() const
  {
    return P_.A2_plus;
  }

  inline void set_A2_plus(const double __v)
  {
    P_.A2_plus = __v;
  }inline double get_A3_plus() const
  {
    return P_.A3_plus;
  }

  inline void set_A3_plus(const double __v)
  {
    P_.A3_plus = __v;
  }inline double get_A2_minus() const
  {
    return P_.A2_minus;
  }

  inline void set_A2_minus(const double __v)
  {
    P_.A2_minus = __v;
  }inline double get_A3_minus() const
  {
    return P_.A3_minus;
  }

  inline void set_A3_minus(const double __v)
  {
    P_.A3_minus = __v;
  }inline double get_Wmax() const
  {
    return P_.Wmax;
  }

  inline void set_Wmax(const double __v)
  {
    P_.Wmax = __v;
  }inline double get_Wmin() const
  {
    return P_.Wmin;
  }

  inline void set_Wmin(const double __v)
  {
    P_.Wmin = __v;
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
  update_internal_state_(double t_start, double timestep, const stdp_triplet_nestml__with_iaf_psc_delta_nestmlCommonSynapseProperties& cp);

  void recompute_internal_variables();

public:
  // this line determines which common properties to use
  typedef stdp_triplet_nestml__with_iaf_psc_delta_nestmlCommonSynapseProperties CommonPropertiesType;

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
  stdp_triplet_nestml__with_iaf_psc_delta_nestml();

  /**
  * Copy constructor from a property object.
  *
  * Sets default values for all parameters (skipping common properties).
  *
  * Needs to be defined properly in order for GenericConnector to work.
  */
  stdp_triplet_nestml__with_iaf_psc_delta_nestml( const stdp_triplet_nestml__with_iaf_psc_delta_nestml& rhs );

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
      dynamic_cast<iaf_psc_delta_nestml__with_stdp_triplet_nestml&>(t);
    }
    catch (std::bad_cast &exp) {
      std::cout << "wrong type of neuron connected! Synapse 'stdp_triplet_nestml__with_iaf_psc_delta_nestml' will only work with neuron 'iaf_psc_delta_nestml__with_stdp_triplet_nestml'.\n";
      exit(1);
    }

    t.register_stdp_connection( t_lastspike_ - get_delay(), get_delay() );
  }
  bool
  send( Event& e, const size_t tid, const stdp_triplet_nestml__with_iaf_psc_delta_nestmlCommonSynapseProperties& cp )
  {
    const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

    auto get_thread = [tid]()
    {
        return tid;
    };

    const double __t_spike = e.get_stamp().get_ms();
#ifdef DEBUG
    std::cout << "stdp_triplet_nestml__with_iaf_psc_delta_nestml::send(): handling pre spike at t = " << __t_spike << std::endl;
#endif
    // use accessor functions (inherited from Connection< >) to obtain delay and target
    iaf_psc_delta_nestml__with_stdp_triplet_nestml* __target = static_cast<iaf_psc_delta_nestml__with_stdp_triplet_nestml*>(get_target(tid));
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
      std::deque< histentry__iaf_psc_delta_nestml__with_stdp_triplet_nestml >::iterator start;
      std::deque< histentry__iaf_psc_delta_nestml__with_stdp_triplet_nestml >::iterator finish;
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
       *  NESTML generated onReceive code block for postsynaptic port "post_spikes" begins here!
      **/
      double w_ = S_.w + S_.tr_r1 * (P_.A2_plus + P_.A3_plus * ((post_neuron_t*)(__target))->get_tr_o2__for_stdp_triplet_nestml(_tr_t));
      S_.w = std::min(P_.Wmax, w_);

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
         *  NESTML generated onReceive code block for presynaptic port "pre_spikes" begins here!
        **/
        S_.tr_r1 += 1;
        S_.tr_r2 += 1;
        double w_ = S_.w - ((post_neuron_t*)(__target))->get_tr_o1__for_stdp_triplet_nestml(_tr_t) * (P_.A2_minus + P_.A3_minus * S_.tr_r2);
        S_.w = std::max(P_.Wmin, w_);

                set_delay( P_.d );
                const long __delay_steps = nest::Time::delay_ms_to_steps( get_delay() );
                set_delay_steps(__delay_steps);
                e.set_receiver( *__target );
          e.set_weight( S_.w );
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
      /**
       *  NESTML generated onReceive code block for postsynaptic port "post_spikes" begins here!
      **/
      double w_ = S_.w + S_.tr_r1 * (P_.A2_plus + P_.A3_plus * ((post_neuron_t*)(__target))->get_tr_o2__for_stdp_triplet_nestml(_tr_t));
      S_.w = std::min(P_.Wmax, w_);
    }

    /**
     *  synapse internal state has now been fully updated to `__t_spike`
    **/

    t_lastspike_ = __t_spike;
    return true;
  }

  void get_status( DictionaryDatum& d ) const;

  void set_status( const DictionaryDatum& d, ConnectorModel& cm );
};
void
register_stdp_triplet_nestml__with_iaf_psc_delta_nestml( const std::string& name )
{
  nest::register_connection_model< stdp_triplet_nestml__with_iaf_psc_delta_nestml >( name );
}
template < typename targetidentifierT >
constexpr ConnectionModelProperties stdp_triplet_nestml__with_iaf_psc_delta_nestml< targetidentifierT >::properties;


template < typename targetidentifierT >
void
stdp_triplet_nestml__with_iaf_psc_delta_nestml< targetidentifierT >::get_status( DictionaryDatum& __d ) const
{
  ConnectionBase::get_status( __d );
  def< long >( __d, names::size_of, sizeof( *this ) );

  // parameters
  def< double >( __d, names::delay, P_.d );  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tau_plus, get_tau_plus());  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tau_x, get_tau_x());  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tau_minus, get_tau_minus());  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tau_y, get_tau_y());  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_A2_plus, get_A2_plus());  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_A3_plus, get_A3_plus());  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_A2_minus, get_A2_minus());  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_A3_minus, get_A3_minus());  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_Wmax, get_Wmax());  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_Wmin, get_Wmin());

  // initial values for state variables in ODE or kernel  
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_w, get_w());
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tr_r1, get_tr_r1());
  def<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tr_r2, get_tr_r2());
}

template < typename targetidentifierT >
void
stdp_triplet_nestml__with_iaf_psc_delta_nestml< targetidentifierT >::set_status( const DictionaryDatum& __d,
  ConnectorModel& cm )
{
  // parameters  
  double tmp_d = get_d();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_d, tmp_d);  
  double tmp_tau_plus = get_tau_plus();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tau_plus, tmp_tau_plus);  
  double tmp_tau_x = get_tau_x();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tau_x, tmp_tau_x);  
  double tmp_tau_minus = get_tau_minus();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tau_minus, tmp_tau_minus);  
  double tmp_tau_y = get_tau_y();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tau_y, tmp_tau_y);  
  double tmp_A2_plus = get_A2_plus();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_A2_plus, tmp_A2_plus);  
  double tmp_A3_plus = get_A3_plus();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_A3_plus, tmp_A3_plus);  
  double tmp_A2_minus = get_A2_minus();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_A2_minus, tmp_A2_minus);  
  double tmp_A3_minus = get_A3_minus();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_A3_minus, tmp_A3_minus);  
  double tmp_Wmax = get_Wmax();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_Wmax, tmp_Wmax);  
  double tmp_Wmin = get_Wmin();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_Wmin, tmp_Wmin);

  // initial values for state variables in ODE or kernel  
  double tmp_w = get_w();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_w, tmp_w);
  double tmp_tr_r1 = get_tr_r1();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tr_r1, tmp_tr_r1);
  double tmp_tr_r2 = get_tr_r2();
  updateValue<double>(__d, nest::stdp_triplet_nestml__with_iaf_psc_delta_nestml_names::_tr_r2, tmp_tr_r2);


  // We now know that (ptmp, stmp) are consistent. We do not
  // write them back to (P_, S_) before we are also sure that
  // the properties to be set in the parent class are internally
  // consistent.
  ConnectionBase::set_status( __d, cm );

  // if we get here, temporaries contain consistent set of properties

  // set parameters  
  set_d(tmp_d);  
  set_tau_plus(tmp_tau_plus);  
  set_tau_x(tmp_tau_x);  
  set_tau_minus(tmp_tau_minus);  
  set_tau_y(tmp_tau_y);  
  set_A2_plus(tmp_A2_plus);  
  set_A3_plus(tmp_A3_plus);  
  set_A2_minus(tmp_A2_minus);  
  set_A3_minus(tmp_A3_minus);  
  set_Wmax(tmp_Wmax);  
  set_Wmin(tmp_Wmin);

  // set state  
  set_w(tmp_w);  
  set_tr_r1(tmp_tr_r1);  
  set_tr_r2(tmp_tr_r2);

  // check invariants



  // special treatment of NEST delay
  set_delay(
get_d());

  // recompute internal variables in case they are dependent on parameters or state that might have been updated in this call to set_status()
  recompute_internal_variables();
}

/**
 * NESTML internals block symbols initialisation
**/
template < typename targetidentifierT >
void stdp_triplet_nestml__with_iaf_psc_delta_nestml< targetidentifierT >::recompute_internal_variables()
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function


    

    V_.__P__tr_r1__tr_r1 = std::exp((-V_.__h) / P_.tau_plus); // as real
    

    V_.__P__tr_r2__tr_r2 = std::exp((-V_.__h) / P_.tau_x); // as real
}

/**
 * constructor
**/
template < typename targetidentifierT >
stdp_triplet_nestml__with_iaf_psc_delta_nestml< targetidentifierT >::stdp_triplet_nestml__with_iaf_psc_delta_nestml() : ConnectionBase()
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  

  P_.d = 1; // as ms
  

  P_.tau_plus = 16.8; // as ms
  

  P_.tau_x = 101; // as ms
  

  P_.tau_minus = 33.7; // as ms
  

  P_.tau_y = 125; // as ms
  

  P_.A2_plus = 7.5e-10; // as real
  

  P_.A3_plus = 0.0093; // as real
  

  P_.A2_minus = 0.007; // as real
  

  P_.A3_minus = 0.00023; // as real
  

  P_.Wmax = 100; // as nS
  

  P_.Wmin = 0; // as nS

  V_.__h = nest::Time::get_resolution().get_ms();
  recompute_internal_variables();

  // initial values for state variables in ODE or kernel
  

  S_.w = 1; // as nS
  

  S_.tr_r1 = 0.0; // as real
  

  S_.tr_r2 = 0.0; // as real

  t_lastspike_ = 0.;
}

/**
 * copy constructor
**/
template < typename targetidentifierT >
stdp_triplet_nestml__with_iaf_psc_delta_nestml< targetidentifierT >::stdp_triplet_nestml__with_iaf_psc_delta_nestml( const stdp_triplet_nestml__with_iaf_psc_delta_nestml< targetidentifierT >& rhs )
: ConnectionBase( rhs )
{
    P_.d = rhs.P_.d;
    P_.tau_plus = rhs.P_.tau_plus;
    P_.tau_x = rhs.P_.tau_x;
    P_.tau_minus = rhs.P_.tau_minus;
    P_.tau_y = rhs.P_.tau_y;
    P_.A2_plus = rhs.P_.A2_plus;
    P_.A3_plus = rhs.P_.A3_plus;
    P_.A2_minus = rhs.P_.A2_minus;
    P_.A3_minus = rhs.P_.A3_minus;
    P_.Wmax = rhs.P_.Wmax;
    P_.Wmin = rhs.P_.Wmin;

  // state variables in ODE or kernel
    S_.w = rhs.S_.w;
    S_.tr_r1 = rhs.S_.tr_r1;
    S_.tr_r2 = rhs.S_.tr_r2;

    //weight_ = get_named_parameter<double>(names::weight);
    //set_weight( *rhs.weight_ );
    t_lastspike_ = rhs.t_lastspike_;

    // special treatment of NEST delay
    set_delay(rhs.get_delay());
}

template < typename targetidentifierT >
inline void
stdp_triplet_nestml__with_iaf_psc_delta_nestml< targetidentifierT >::update_internal_state_(double t_start, double timestep, const stdp_triplet_nestml__with_iaf_psc_delta_nestmlCommonSynapseProperties& cp)
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
  double tr_r1__tmp = V_.__P__tr_r1__tr_r1 * S_.tr_r1;
  double tr_r2__tmp = V_.__P__tr_r2__tr_r2 * S_.tr_r2;
  /* replace analytically solvable variables with precisely integrated values  */
  S_.tr_r1 = tr_r1__tmp;
  S_.tr_r2 = tr_r2__tmp;
    V_.__h = old___h;
    recompute_internal_variables();  // XXX: can be skipped?

    // NESTML generated code for the update block:
}

} // namespace

#endif /* #ifndef STDP_TRIPLET_NESTML__WITH_IAF_PSC_DELTA_NESTML_H */