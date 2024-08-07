// #define DEBUG 1
/*
 *  gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml.cpp
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
 *  Generated from NESTML at time: 2024-02-26 10:21:47.866896
**/

// C++ includes:
#include <limits>

// Includes from libnestutil:
#include "numerics.h"

// Includes from nestkernel:
#include "exceptions.h"
#include "kernel_manager.h"
#include "universal_data_logger_impl.h"

// Includes from sli:
#include "dict.h"
#include "dictutils.h"
#include "doubledatum.h"
#include "integerdatum.h"
#include "lockptrdatum.h"

#include "gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml.h"

// ---------------------------------------------------------------------------
//   Recordables map
// ---------------------------------------------------------------------------
nest::RecordablesMap<gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml> gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::recordablesMap_;
namespace nest
{

  // Override the create() method with one call to RecordablesMap::insert_()
  // for each quantity to be recorded.
template <> void RecordablesMap<gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml>::create()
  {
    // add state variables to recordables map
   insert_(gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml_names::_U, &gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::get_U);

    // Add vector variables  
  }
}

// ---------------------------------------------------------------------------
//   Default constructors defining default parameters and state
//   Note: the implementation is empty. The initialization is of variables
//   is a part of gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml's constructor.
// ---------------------------------------------------------------------------

gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::Parameters_::Parameters_()
{
}

gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::State_::State_()
{
}

// ---------------------------------------------------------------------------
//   Parameter and state extractions and manipulation functions
// ---------------------------------------------------------------------------

gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::Buffers_::Buffers_(gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::Buffers_::Buffers_(const Buffers_ &, gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

// ---------------------------------------------------------------------------
//   Default constructor for node
// ---------------------------------------------------------------------------

gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml():StructuralPlasticityNode(), P_(), S_(), B_(*this)
{
  init_state_internal_();
  recordablesMap_.create();
  pre_run_hook();
}

// ---------------------------------------------------------------------------
//   Copy constructor for node
// ---------------------------------------------------------------------------

gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml(const gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml& __n):
  StructuralPlasticityNode(), P_(__n.P_), S_(__n.S_), B_(__n.B_, *this) {

  // copy parameter struct P_
  P_.a = __n.P_.a;
  P_.alpha_over_N = __n.P_.alpha_over_N;
  P_.beta = __n.P_.beta;
  P_.reset_after_spike = __n.P_.reset_after_spike;

  // copy state struct S_
  S_.U = __n.S_.U;

  // copy internals V_
  V_.__h = __n.V_.__h;
  V_.__P__U__U = __n.V_.__P__U__U;
  n_incoming_ = __n.n_incoming_;
  max_delay_ = __n.max_delay_;
  last_spike_ = __n.last_spike_;

  // cache initial values
}

// ---------------------------------------------------------------------------
//   Destructor for node
// ---------------------------------------------------------------------------

gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::~gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml()
{
}

// ---------------------------------------------------------------------------
//   Node initialization functions
// ---------------------------------------------------------------------------
void gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::calibrate_time( const nest::TimeConverter& tc )
{
  LOG( nest::M_WARNING,
    "gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml",
    "Simulation resolution has changed. Internal state and parameters of the model have been reset!" );

  init_state_internal_();
}
void gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::init_state_internal_()
{
#ifdef DEBUG
  std::cout << "gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::init_state_internal_()" << std::endl;
#endif

  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  // initial values for parameters
    

    P_.a = 3.0; // as real
    

    P_.alpha_over_N = 1.0777744654743957; // as real
    

    P_.beta = 50; // as real
    

    P_.reset_after_spike = true; // as boolean

  recompute_internal_variables();
  // initial values for state variables
    

    S_.U = 0; // as real
  // state variables for archiving state for paired synapse
  n_incoming_ = 0;
  max_delay_ = 0;
  last_spike_ = -1.;

  // cache initial values
}

void gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::init_buffers_()
{
#ifdef DEBUG
  std::cout << "gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::init_buffers_()" << std::endl;
#endif
  // spike input buffers
  get_spike_inputs_().clear();
  get_spike_inputs_grid_sum_().clear();

  B_.logger_.reset();


}

void gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::recompute_internal_variables(bool exclude_timestep) {
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

  if (exclude_timestep) {    
      

      V_.__P__U__U = 1.0 * std::exp((-0.001) * V_.__h * P_.beta); // as real
  }
  else {    
      

      V_.__h = __resolution; // as ms
      

      V_.__P__U__U = 1.0 * std::exp((-0.001) * V_.__h * P_.beta); // as real
  }
}
void gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::pre_run_hook() {
  B_.logger_.init();

  // parameters might have changed -- recompute internals
  recompute_internal_variables();

  // buffers B_
  B_.spike_inputs_.resize(NUM_SPIKE_RECEPTORS);
  B_.spike_inputs_grid_sum_.resize(NUM_SPIKE_RECEPTORS);
}

// ---------------------------------------------------------------------------
//   Functions defined in the NESTML model
// ---------------------------------------------------------------------------

//
double gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::phi ( double U) const
{  
  if (U <= 0)
  {  
    return 0;
  }
  return (4 * P_.a) / (1 + std::exp(P_.a - U)) - (4 * P_.a) / (1 + std::exp(P_.a));
}

// ---------------------------------------------------------------------------
//   Update and spike handling functions
// ---------------------------------------------------------------------------


void gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::update(nest::Time const & origin,const long from, const long to)
{
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function



  for ( long lag = from ; lag < to ; ++lag )
  {
    auto get_t = [origin, lag](){ return nest::Time( nest::Time::step( origin.get_steps() + lag + 1) ).get_ms(); };

    for (long i = 0; i < NUM_SPIKE_RECEPTORS; ++i)
    {
        get_spike_inputs_grid_sum_()[i] = get_spike_inputs_()[i].get_value(lag);
    }

    // NESTML generated code for the update block
  double U__tmp = S_.U * V_.__P__U__U;
  /* replace analytically solvable variables with precisely integrated values  */
  S_.U = U__tmp;
  S_.U += (P_.alpha_over_N / 1.0) * (0.001 * B_.spike_inputs_grid_sum_[INCOMING_SPIKES - MIN_SPIKE_RECEPTOR]) / (1 / 1000.0);
  if (((0) + (1) * nest::get_vp_specific_rng( get_thread() )->drand()) <= 0.001 * __resolution * phi(S_.U))
  {  
    set_spiketime(nest::Time::step(origin.get_steps()+lag+1));
    nest::SpikeEvent se;
    nest::kernel().event_delivery_manager.send(*this, se, lag);
    if (P_.reset_after_spike)
    {  
      S_.U = 0;
    }
  }
    // voltage logging
    B_.logger_.record_data(origin.get_steps() + lag);
  }
}

// Do not move this function as inline to h-file. It depends on
// universal_data_logger_impl.h being included here.
void gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::handle(nest::DataLoggingRequest& e)
{
  B_.logger_.handle(e);
}


void gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::handle(nest::SpikeEvent &e)
{
  assert(e.get_delay_steps() > 0);
  assert( e.get_rport() < B_.spike_inputs_.size() );

  double weight = e.get_weight();
  size_t nestml_buffer_idx = 0;
  B_.spike_inputs_[ nestml_buffer_idx - MIN_SPIKE_RECEPTOR ].add_value(
    e.get_rel_delivery_steps( nest::kernel().simulation_manager.get_slice_origin() ),
    weight * e.get_multiplicity() );
}


inline double
gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::get_spiketime_ms() const
{
  return last_spike_;
}


void
gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::register_stdp_connection( double t_first_read, double delay )
{
  // Mark all entries in the deque, which we will not read in future as read by
  // this input input, so that we safely increment the incoming number of
  // connections afterwards without leaving spikes in the history.
  // For details see bug #218. MH 08-04-22

  for ( std::deque< histentry__gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml >::iterator runner = history_.begin();
        runner != history_.end() and ( t_first_read - runner->t_ > -1.0 * nest::kernel().connection_manager.get_stdp_eps() );
        ++runner )
  {
    ( runner->access_counter_ )++;
  }

  n_incoming_++;

  max_delay_ = std::max( delay, max_delay_ );
}


void
gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::get_history__( double t1,
  double t2,
  std::deque< histentry__gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml >::iterator* start,
  std::deque< histentry__gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml >::iterator* finish )
{
  *finish = history_.end();
  if ( history_.empty() )
  {
    *start = *finish;
    return;
  }
  std::deque< histentry__gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml >::reverse_iterator runner = history_.rbegin();
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
gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::set_spiketime( nest::Time const& t_sp, double offset )
{
    StructuralPlasticityNode::set_spiketime( t_sp, offset );

    unsigned int num_transferred_variables = 0;

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
        }
        else {
        }


        /**
         * update state variables transferred from synapse from `last_spike_` to `t_sp_ms`
        **/

        const double old___h = V_.__h;
        V_.__h = t_sp_ms - last_spike_;
        if (V_.__h > 1E-12) {
          recompute_internal_variables(true);
      
      /* replace analytically solvable variables with precisely integrated values  */
        V_.__h = old___h;
        recompute_internal_variables(true);
      }

        /**
         * apply spike updates
        **/

    last_spike_ = t_sp_ms;
    history_.push_back( histentry__gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml( last_spike_
, 0
 ) );
  }
  else
  {
    last_spike_ = t_sp_ms;
  }
}


void
gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml__with_syn_gl_cac582d906cfdd4f76a2f0e5036501ac82_nestml::clear_history()
{
  last_spike_ = -1.0;
  history_.clear();
}




