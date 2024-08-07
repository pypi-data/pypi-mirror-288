// #define DEBUG 1
/*
 *  iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml.cpp
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
 *  Generated from NESTML at time: 2024-04-04 08:52:40.966032
**/

// C++ includes:
#include <limits>

// Includes from libnestutil:
#include "numerics.h"

// Includes from nestkernel:
#include "exceptions.h"
#include "kernel_manager.h"
#include "nest_impl.h"
#include "universal_data_logger_impl.h"

// Includes from sli:
#include "dict.h"
#include "dictutils.h"
#include "doubledatum.h"
#include "integerdatum.h"
#include "lockptrdatum.h"

#include "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml.h"
void
register_iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml( const std::string& name )
{
  nest::register_node_model< iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml >( name );
}

// ---------------------------------------------------------------------------
//   Recordables map
// ---------------------------------------------------------------------------
nest::RecordablesMap<iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml> iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::recordablesMap_;
namespace nest
{

  // Override the create() method with one call to RecordablesMap::insert_()
  // for each quantity to be recorded.
template <> void RecordablesMap<iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml>::create()
  {
    // add state variables to recordables map
   insert_(iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml_names::_refr_spikes_buffer, &iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_refr_spikes_buffer);
   insert_(iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml_names::_V_m, &iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_V_m);
   insert_(iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml_names::_post_tr__for_neuromodulated_stdp_nestml, &iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_post_tr__for_neuromodulated_stdp_nestml);

    // Add vector variables  
  }
}

// ---------------------------------------------------------------------------
//   Default constructors defining default parameters and state
//   Note: the implementation is empty. The initialization is of variables
//   is a part of iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml's constructor.
// ---------------------------------------------------------------------------

iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::Parameters_::Parameters_()
{
}

iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::State_::State_()
{
}

// ---------------------------------------------------------------------------
//   Parameter and state extractions and manipulation functions
// ---------------------------------------------------------------------------

iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::Buffers_::Buffers_(iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::Buffers_::Buffers_(const Buffers_ &, iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

// ---------------------------------------------------------------------------
//   Default constructor for node
// ---------------------------------------------------------------------------

iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml():StructuralPlasticityNode(), P_(), S_(), B_(*this)
{
  init_state_internal_();
  recordablesMap_.create();
  pre_run_hook();
}

// ---------------------------------------------------------------------------
//   Copy constructor for node
// ---------------------------------------------------------------------------

iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml(const iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml& __n):
  StructuralPlasticityNode(), P_(__n.P_), S_(__n.S_), B_(__n.B_, *this) {

  // copy parameter struct P_
  P_.tau_m = __n.P_.tau_m;
  P_.C_m = __n.P_.C_m;
  P_.t_ref = __n.P_.t_ref;
  P_.tau_syn = __n.P_.tau_syn;
  P_.E_L = __n.P_.E_L;
  P_.V_reset = __n.P_.V_reset;
  P_.V_th = __n.P_.V_th;
  P_.V_min = __n.P_.V_min;
  P_.with_refr_input = __n.P_.with_refr_input;
  P_.I_e = __n.P_.I_e;
  P_.tau_tr_post__for_neuromodulated_stdp_nestml = __n.P_.tau_tr_post__for_neuromodulated_stdp_nestml;

  // copy state struct S_
  S_.refr_spikes_buffer = __n.S_.refr_spikes_buffer;
  S_.r = __n.S_.r;
  S_.V_m = __n.S_.V_m;
  S_.post_tr__for_neuromodulated_stdp_nestml = __n.S_.post_tr__for_neuromodulated_stdp_nestml;

  // copy internals V_
  V_.h = __n.V_.h;
  V_.__h = __n.V_.__h;
  V_.RefractoryCounts = __n.V_.RefractoryCounts;
  V_.__P__V_m__V_m = __n.V_.__P__V_m__V_m;
  V_.__P__post_tr__for_neuromodulated_stdp_nestml__post_tr__for_neuromodulated_stdp_nestml = __n.V_.__P__post_tr__for_neuromodulated_stdp_nestml__post_tr__for_neuromodulated_stdp_nestml;
  n_incoming_ = __n.n_incoming_;
  max_delay_ = __n.max_delay_;
  last_spike_ = __n.last_spike_;

  // cache initial values
  post_tr__for_neuromodulated_stdp_nestml__iv = S_.post_tr__for_neuromodulated_stdp_nestml;
}

// ---------------------------------------------------------------------------
//   Destructor for node
// ---------------------------------------------------------------------------

iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::~iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml()
{
}

// ---------------------------------------------------------------------------
//   Node initialization functions
// ---------------------------------------------------------------------------
void iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::calibrate_time( const nest::TimeConverter& tc )
{
  LOG( nest::M_WARNING,
    "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml",
    "Simulation resolution has changed. Internal state and parameters of the model have been reset!" );

  init_state_internal_();
}
void iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::init_state_internal_()
{
#ifdef DEBUG
  std::cout << "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::init_state_internal_()" << std::endl;
#endif

  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  // initial values for parameters
    

    P_.tau_m = 10; // as ms
    

    P_.C_m = 250; // as pF
    

    P_.t_ref = 2; // as ms
    

    P_.tau_syn = 2; // as ms
    

    P_.E_L = (-70); // as mV
    

    P_.V_reset = (-70); // as mV
    

    P_.V_th = (-55); // as mV
    

    P_.V_min = (-std::numeric_limits< double_t >::infinity()) * 1; // as mV
    

    P_.with_refr_input = false; // as boolean
    

    P_.I_e = 0; // as pA
    

    P_.tau_tr_post__for_neuromodulated_stdp_nestml = 20; // as ms

  recompute_internal_variables();
  // initial values for state variables
    

    S_.refr_spikes_buffer = 0; // as mV
    

    S_.r = 0; // as integer
    

    S_.V_m = P_.E_L; // as mV
    

    S_.post_tr__for_neuromodulated_stdp_nestml = 0.0; // as real
  // state variables for archiving state for paired synapse
  n_incoming_ = 0;
  max_delay_ = 0;
  last_spike_ = -1.;

  // cache initial values
  post_tr__for_neuromodulated_stdp_nestml__iv = S_.post_tr__for_neuromodulated_stdp_nestml;
}

void iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::init_buffers_()
{
#ifdef DEBUG
  std::cout << "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::init_buffers_()" << std::endl;
#endif
  // spike input buffers
  get_spike_inputs_().clear();
  get_spike_inputs_grid_sum_().clear();

  // continuous time input buffers  

  get_I_stim().clear();
  B_.I_stim_grid_sum_ = 0;

  B_.logger_.reset();


}

void iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::recompute_internal_variables(bool exclude_timestep) {
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

  if (exclude_timestep) {    
      

      V_.h = __resolution; // as ms
      

      V_.RefractoryCounts = nest::Time(nest::Time::ms((double) (P_.t_ref))).get_steps(); // as integer
      

      V_.__P__V_m__V_m = std::exp((-V_.__h) / P_.tau_m); // as real
      

      V_.__P__post_tr__for_neuromodulated_stdp_nestml__post_tr__for_neuromodulated_stdp_nestml = std::exp((-V_.__h) / P_.tau_tr_post__for_neuromodulated_stdp_nestml); // as real
  }
  else {    
      

      V_.h = __resolution; // as ms
      

      V_.__h = __resolution; // as ms
      

      V_.RefractoryCounts = nest::Time(nest::Time::ms((double) (P_.t_ref))).get_steps(); // as integer
      

      V_.__P__V_m__V_m = std::exp((-V_.__h) / P_.tau_m); // as real
      

      V_.__P__post_tr__for_neuromodulated_stdp_nestml__post_tr__for_neuromodulated_stdp_nestml = std::exp((-V_.__h) / P_.tau_tr_post__for_neuromodulated_stdp_nestml); // as real
  }
}
void iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::pre_run_hook() {
  B_.logger_.init();

  // parameters might have changed -- recompute internals
  recompute_internal_variables();

  // buffers B_
  B_.spike_inputs_.resize(NUM_SPIKE_RECEPTORS);
  B_.spike_inputs_grid_sum_.resize(NUM_SPIKE_RECEPTORS);
}

// ---------------------------------------------------------------------------
//   Update and spike handling functions
// ---------------------------------------------------------------------------


void iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::update(nest::Time const & origin,const long from, const long to)
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function



  for ( long lag = from ; lag < to ; ++lag )
  {
    auto get_t = [origin, lag](){ return nest::Time( nest::Time::step( origin.get_steps() + lag + 1) ).get_ms(); };

    for (long i = 0; i < NUM_SPIKE_RECEPTORS; ++i)
    {
        get_spike_inputs_grid_sum_()[i] = get_spike_inputs_()[i].get_value(lag);
    }
    B_.I_stim_grid_sum_ = get_I_stim().get_value(lag);

    // NESTML generated code for the update block
  if (S_.r == 0)
  {  
    double V_m__tmp = (-P_.E_L) * V_.__P__V_m__V_m + P_.E_L + S_.V_m * V_.__P__V_m__V_m - P_.I_e * V_.__P__V_m__V_m * P_.tau_m / P_.C_m + P_.I_e * P_.tau_m / P_.C_m - B_.I_stim_grid_sum_ * V_.__P__V_m__V_m * P_.tau_m / P_.C_m + B_.I_stim_grid_sum_ * P_.tau_m / P_.C_m;
    /* replace analytically solvable variables with precisely integrated values  */
    S_.V_m = V_m__tmp;
    S_.V_m += (1.0 / 1.0) * (0.001 * B_.spike_inputs_grid_sum_[SPIKES - MIN_SPIKE_RECEPTOR]) / (1 / 1000.0);
    if (P_.with_refr_input && S_.refr_spikes_buffer != 0.0)
    {  
      S_.V_m += S_.refr_spikes_buffer;
      S_.refr_spikes_buffer = 0.0;
    }
    S_.V_m = (S_.V_m < P_.V_min) ? (P_.V_min) : (S_.V_m);
  }
  else
  {  
    if (P_.with_refr_input)
    {  
      S_.refr_spikes_buffer += (0.001 * B_.spike_inputs_grid_sum_[SPIKES - MIN_SPIKE_RECEPTOR]) * 1000.0 * std::exp((-S_.r) * V_.h / P_.tau_m) * 1.0;
    }
    S_.r -= 1;
  }
  if (S_.V_m >= P_.V_th)
  {  
    S_.r = V_.RefractoryCounts;
    S_.V_m = P_.V_reset;
    set_spiketime(nest::Time::step(origin.get_steps()+lag+1));
    nest::SpikeEvent se;
    nest::kernel().event_delivery_manager.send(*this, se, lag);
  }
    // voltage logging
    B_.logger_.record_data(origin.get_steps() + lag);
  }
}

// Do not move this function as inline to h-file. It depends on
// universal_data_logger_impl.h being included here.
void iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::handle(nest::DataLoggingRequest& e)
{
  B_.logger_.handle(e);
}


void iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::handle(nest::SpikeEvent &e)
{
  assert(e.get_delay_steps() > 0);
  assert( e.get_rport() < B_.spike_inputs_.size() );

  double weight = e.get_weight();
  size_t nestml_buffer_idx = 0;
  B_.spike_inputs_[ nestml_buffer_idx - MIN_SPIKE_RECEPTOR ].add_value(
    e.get_rel_delivery_steps( nest::kernel().simulation_manager.get_slice_origin() ),
    weight * e.get_multiplicity() );
}

void iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::handle(nest::CurrentEvent& e)
{
  assert(e.get_delay_steps() > 0);

  const double current = e.get_current();     // we assume that in NEST, this returns a current in pA
  const double weight = e.get_weight();
  get_I_stim().add_value(
               e.get_rel_delivery_steps( nest::kernel().simulation_manager.get_slice_origin()),
               weight * current );
}


inline double
iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_spiketime_ms() const
{
  return last_spike_;
}


void
iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::register_stdp_connection( double t_first_read, double delay )
{
  // Mark all entries in the deque, which we will not read in future as read by
  // this input input, so that we safely increment the incoming number of
  // connections afterwards without leaving spikes in the history.
  // For details see bug #218. MH 08-04-22

  for ( std::deque< histentry__iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml >::iterator runner = history_.begin();
        runner != history_.end() and ( t_first_read - runner->t_ > -1.0 * nest::kernel().connection_manager.get_stdp_eps() );
        ++runner )
  {
    ( runner->access_counter_ )++;
  }

  n_incoming_++;

  max_delay_ = std::max( delay, max_delay_ );
}


void
iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_history__( double t1,
  double t2,
  std::deque< histentry__iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml >::iterator* start,
  std::deque< histentry__iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml >::iterator* finish )
{
  *finish = history_.end();
  if ( history_.empty() )
  {
    *start = *finish;
    return;
  }
  std::deque< histentry__iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml >::reverse_iterator runner = history_.rbegin();
  const double t2_lim = t2 + nest::kernel().connection_manager.get_stdp_eps();
  const double t1_lim = t1 + nest::kernel().connection_manager.get_stdp_eps();
  while ( runner != history_.rend() and runner->t_ >= t2_lim )
  {
    ++runner;
  }
  *finish = runner.base();
  while ( runner != history_.rend() and runner->t_ >= t1_lim )
  {
    runner->access_counter_++;
    ++runner;
  }
  *start = runner.base();
}

void
iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::set_spiketime( nest::Time const& t_sp, double offset )
{
    StructuralPlasticityNode::set_spiketime( t_sp, offset );

    unsigned int num_transferred_variables = 0;
    ++num_transferred_variables;

    const double t_sp_ms = t_sp.get_ms() - offset;

    if ( n_incoming_ )
    {
        // prune all spikes from history which are no longer needed
        // only remove a spike if:
        // - its access counter indicates it has been read out by all connected
        //     STDP synapses, and
        // - there is another, later spike, that is strictly more than
        //     (min_global_delay + max_delay_ + eps) away from the new spike (at t_sp_ms)
        while ( history_.size() > 1 )
        {
            const double next_t_sp = history_[ 1 ].t_;
            if ( history_.front().access_counter_ >= n_incoming_ * num_transferred_variables
                 and t_sp_ms - next_t_sp > max_delay_ + nest::Time::delay_steps_to_ms(nest::kernel().connection_manager.get_min_delay()) + nest::kernel().connection_manager.get_stdp_eps() )
            {
                history_.pop_front();
            }
            else
            {
                break;
            }
        }

        if (history_.size() > 0) {
            assert(history_.back().t_ == last_spike_);
            S_.post_tr__for_neuromodulated_stdp_nestml = history_.back().post_tr__for_neuromodulated_stdp_nestml_;
        }
        else {
            S_.post_tr__for_neuromodulated_stdp_nestml = 0.; // initial value for convolution is always 0
        }


        /**
         * update state variables transferred from synapse from `last_spike_` to `t_sp_ms`
        **/

        const double old___h = V_.__h;
        V_.__h = t_sp_ms - last_spike_;
        if (V_.__h > 1E-12) {
          recompute_internal_variables(true);
      
      double post_tr__for_neuromodulated_stdp_nestml__tmp = V_.__P__post_tr__for_neuromodulated_stdp_nestml__post_tr__for_neuromodulated_stdp_nestml * S_.post_tr__for_neuromodulated_stdp_nestml;
      /* replace analytically solvable variables with precisely integrated values  */
      S_.post_tr__for_neuromodulated_stdp_nestml = post_tr__for_neuromodulated_stdp_nestml__tmp;
        V_.__h = old___h;
        recompute_internal_variables(true);
      }

        /**
         * apply spike updates
        **/
        S_.post_tr__for_neuromodulated_stdp_nestml += 1.0;

    last_spike_ = t_sp_ms;
    history_.push_back( histentry__iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml( last_spike_
    , get_post_tr__for_neuromodulated_stdp_nestml()
, 0
 ) );
  }
  else
  {
    last_spike_ = t_sp_ms;
  }
}


void
iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::clear_history()
{
  last_spike_ = -1.0;
  history_.clear();
}




double
iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_post_tr__for_neuromodulated_stdp_nestml( double t, const bool before_increment )
{
#ifdef DEBUG
  std::cout << "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_post_tr__for_neuromodulated_stdp_nestml: getting value at t = " << t << std::endl;
#endif

  // case when the neuron has not yet spiked
  if ( history_.empty() )
  {
#ifdef DEBUG
    std::cout << "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_post_tr__for_neuromodulated_stdp_nestml: \thistory empty, returning initial value = " << post_tr__for_neuromodulated_stdp_nestml__iv << std::endl;
#endif
    // return initial value
    return post_tr__for_neuromodulated_stdp_nestml__iv;
  }

  // search for the latest post spike in the history buffer that came strictly before `t`
  int i = history_.size() - 1;
  double eps = 0.;
  if ( before_increment ) {
   eps = nest::kernel().connection_manager.get_stdp_eps();
  }
  while ( i >= 0 )
  {
    if ( t - history_[ i ].t_ >= eps )
    {
#ifdef DEBUG
      std::cout<<"iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_post_tr__for_neuromodulated_stdp_nestml: \tspike occurred at history[i].t_ = " << history_[i].t_ << std::endl;
#endif
      S_.post_tr__for_neuromodulated_stdp_nestml = history_[ i ].post_tr__for_neuromodulated_stdp_nestml_;

      /**
       * update state variables transferred from synapse from `history[i].t_` to `t`
      **/

      if ( t - history_[ i ].t_ >= nest::kernel().connection_manager.get_stdp_eps() )
      {
        const double old___h = V_.__h;
        V_.__h = t - history_[i].t_;
        assert(V_.__h > 0);
        recompute_internal_variables(true);
      
      double post_tr__for_neuromodulated_stdp_nestml__tmp = V_.__P__post_tr__for_neuromodulated_stdp_nestml__post_tr__for_neuromodulated_stdp_nestml * S_.post_tr__for_neuromodulated_stdp_nestml;
      /* replace analytically solvable variables with precisely integrated values  */
      S_.post_tr__for_neuromodulated_stdp_nestml = post_tr__for_neuromodulated_stdp_nestml__tmp;

        V_.__h = old___h;
        recompute_internal_variables(true);
      }

#ifdef DEBUG
      std::cout << "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_post_tr__for_neuromodulated_stdp_nestml: \treturning " << S_.post_tr__for_neuromodulated_stdp_nestml << std::endl;
#endif
      return S_.post_tr__for_neuromodulated_stdp_nestml;       // type: double
    }
    --i;
  }

  // this case occurs when the trace was requested at a time precisely at that of the first spike in the history
  if ( (!before_increment) and t == history_[ 0 ].t_)
  {
    S_.post_tr__for_neuromodulated_stdp_nestml = history_[ 0 ].post_tr__for_neuromodulated_stdp_nestml_;

#ifdef DEBUG
    std::cout << "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_post_tr__for_neuromodulated_stdp_nestml: \ttrace requested at exact time of history entry 0, returning " << S_.post_tr__for_neuromodulated_stdp_nestml << std::endl;
#endif
    return S_.post_tr__for_neuromodulated_stdp_nestml;
  }

  // this case occurs when the trace was requested at a time before the first spike in the history
  // return initial value propagated in time
#ifdef DEBUG
  std::cout << "iaf_psc_delta_nestml__with_neuromodulated_stdp_nestml::get_post_tr__for_neuromodulated_stdp_nestml: \tfall-through, returning initial value = " << post_tr__for_neuromodulated_stdp_nestml__iv << std::endl;
#endif

  if (t == 0.) {
    return 0.;  // initial value for convolution is always 0
  }

  // set to initial value
  S_.post_tr__for_neuromodulated_stdp_nestml = 0.;  // initial value for convolution is always 0

  // propagate in time
  const double old___h = V_.__h;
  V_.__h = t;   // from time 0 to the requested time
  assert(V_.__h > 0);
  recompute_internal_variables(true);
  
  double post_tr__for_neuromodulated_stdp_nestml__tmp = V_.__P__post_tr__for_neuromodulated_stdp_nestml__post_tr__for_neuromodulated_stdp_nestml * S_.post_tr__for_neuromodulated_stdp_nestml;
  /* replace analytically solvable variables with precisely integrated values  */
  S_.post_tr__for_neuromodulated_stdp_nestml = post_tr__for_neuromodulated_stdp_nestml__tmp;
  V_.__h = old___h;
  recompute_internal_variables(true);

  return S_.post_tr__for_neuromodulated_stdp_nestml;
}

