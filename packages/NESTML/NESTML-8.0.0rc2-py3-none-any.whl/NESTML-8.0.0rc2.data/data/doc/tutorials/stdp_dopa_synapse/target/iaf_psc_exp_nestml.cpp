// #define DEBUG 1
/*
 *  iaf_psc_exp_nestml.cpp
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
 *  Generated from NESTML at time: 2024-04-04 08:53:08.792679
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

#include "iaf_psc_exp_nestml.h"
void
register_iaf_psc_exp_nestml( const std::string& name )
{
  nest::register_node_model< iaf_psc_exp_nestml >( name );
}

// ---------------------------------------------------------------------------
//   Recordables map
// ---------------------------------------------------------------------------
nest::RecordablesMap<iaf_psc_exp_nestml> iaf_psc_exp_nestml::recordablesMap_;
namespace nest
{

  // Override the create() method with one call to RecordablesMap::insert_()
  // for each quantity to be recorded.
template <> void RecordablesMap<iaf_psc_exp_nestml>::create()
  {
    // add state variables to recordables map
   insert_(iaf_psc_exp_nestml_names::_V_m, &iaf_psc_exp_nestml::get_V_m);
   insert_(iaf_psc_exp_nestml_names::_I_kernel_exc__X__exc_spikes, &iaf_psc_exp_nestml::get_I_kernel_exc__X__exc_spikes);
   insert_(iaf_psc_exp_nestml_names::_I_kernel_inh__X__inh_spikes, &iaf_psc_exp_nestml::get_I_kernel_inh__X__inh_spikes);

    // Add vector variables  
  }
}
std::vector< std::tuple< int, int > > iaf_psc_exp_nestml::rport_to_nestml_buffer_idx =
{
  
  { iaf_psc_exp_nestml::EXC_SPIKES, iaf_psc_exp_nestml::INH_SPIKES },
};

// ---------------------------------------------------------------------------
//   Default constructors defining default parameters and state
//   Note: the implementation is empty. The initialization is of variables
//   is a part of iaf_psc_exp_nestml's constructor.
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::Parameters_::Parameters_()
{
}

iaf_psc_exp_nestml::State_::State_()
{
}

// ---------------------------------------------------------------------------
//   Parameter and state extractions and manipulation functions
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::Buffers_::Buffers_(iaf_psc_exp_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

iaf_psc_exp_nestml::Buffers_::Buffers_(const Buffers_ &, iaf_psc_exp_nestml &n):
  logger_(n)
  , spike_inputs_( std::vector< nest::RingBuffer >( NUM_SPIKE_RECEPTORS ) )
  , spike_inputs_grid_sum_( std::vector< double >( NUM_SPIKE_RECEPTORS ) )
{
  // Initialization of the remaining members is deferred to init_buffers_().
}

// ---------------------------------------------------------------------------
//   Default constructor for node
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::iaf_psc_exp_nestml():StructuralPlasticityNode(), P_(), S_(), B_(*this)
{
  init_state_internal_();
  recordablesMap_.create();
  pre_run_hook();
}

// ---------------------------------------------------------------------------
//   Copy constructor for node
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::iaf_psc_exp_nestml(const iaf_psc_exp_nestml& __n):
  StructuralPlasticityNode(), P_(__n.P_), S_(__n.S_), B_(__n.B_, *this) {

  // copy parameter struct P_
  P_.C_m = __n.P_.C_m;
  P_.tau_m = __n.P_.tau_m;
  P_.tau_syn_inh = __n.P_.tau_syn_inh;
  P_.tau_syn_exc = __n.P_.tau_syn_exc;
  P_.t_ref = __n.P_.t_ref;
  P_.E_L = __n.P_.E_L;
  P_.V_reset = __n.P_.V_reset;
  P_.V_th = __n.P_.V_th;
  P_.I_e = __n.P_.I_e;

  // copy state struct S_
  S_.r = __n.S_.r;
  S_.V_m = __n.S_.V_m;
  S_.I_kernel_exc__X__exc_spikes = __n.S_.I_kernel_exc__X__exc_spikes;
  S_.I_kernel_inh__X__inh_spikes = __n.S_.I_kernel_inh__X__inh_spikes;

  // copy internals V_
  V_.RefractoryCounts = __n.V_.RefractoryCounts;
  V_.__h = __n.V_.__h;
  V_.__P__V_m__V_m = __n.V_.__P__V_m__V_m;
  V_.__P__V_m__I_kernel_exc__X__exc_spikes = __n.V_.__P__V_m__I_kernel_exc__X__exc_spikes;
  V_.__P__V_m__I_kernel_inh__X__inh_spikes = __n.V_.__P__V_m__I_kernel_inh__X__inh_spikes;
  V_.__P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes = __n.V_.__P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes;
  V_.__P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes = __n.V_.__P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes;
}

// ---------------------------------------------------------------------------
//   Destructor for node
// ---------------------------------------------------------------------------

iaf_psc_exp_nestml::~iaf_psc_exp_nestml()
{
}

// ---------------------------------------------------------------------------
//   Node initialization functions
// ---------------------------------------------------------------------------
void iaf_psc_exp_nestml::calibrate_time( const nest::TimeConverter& tc )
{
  LOG( nest::M_WARNING,
    "iaf_psc_exp_nestml",
    "Simulation resolution has changed. Internal state and parameters of the model have been reset!" );

  init_state_internal_();
}
void iaf_psc_exp_nestml::init_state_internal_()
{
#ifdef DEBUG
  std::cout << "iaf_psc_exp_nestml::init_state_internal_()" << std::endl;
#endif

  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function
  // initial values for parameters
    

    P_.C_m = 250; // as pF
    

    P_.tau_m = 10; // as ms
    

    P_.tau_syn_inh = 2; // as ms
    

    P_.tau_syn_exc = 2; // as ms
    

    P_.t_ref = 2; // as ms
    

    P_.E_L = (-70); // as mV
    

    P_.V_reset = (-70); // as mV
    

    P_.V_th = (-55); // as mV
    

    P_.I_e = 0; // as pA

  recompute_internal_variables();
  // initial values for state variables
    

    S_.r = 0; // as integer
    

    S_.V_m = P_.E_L; // as mV
    

    S_.I_kernel_exc__X__exc_spikes = 0; // as real
    

    S_.I_kernel_inh__X__inh_spikes = 0; // as real
}

void iaf_psc_exp_nestml::init_buffers_()
{
#ifdef DEBUG
  std::cout << "iaf_psc_exp_nestml::init_buffers_()" << std::endl;
#endif
  // spike input buffers
  get_spike_inputs_().clear();
  get_spike_inputs_grid_sum_().clear();

  // continuous time input buffers  

  get_I_stim().clear();
  B_.I_stim_grid_sum_ = 0;

  B_.logger_.reset();


}

void iaf_psc_exp_nestml::recompute_internal_variables(bool exclude_timestep) {
  const double __resolution = nest::Time::get_resolution().get_ms();  // do not remove, this is necessary for the resolution() function

  if (exclude_timestep) {    
      

      V_.RefractoryCounts = nest::Time(nest::Time::ms((double) (P_.t_ref))).get_steps(); // as integer
      

      V_.__P__V_m__V_m = 1.0 * std::exp((-V_.__h) / P_.tau_m); // as real
      

      V_.__P__V_m__I_kernel_exc__X__exc_spikes = 1.0 * P_.tau_m * P_.tau_syn_exc * ((-std::exp(V_.__h / P_.tau_m)) + std::exp(V_.__h / P_.tau_syn_exc)) * std::exp((-V_.__h) * (P_.tau_m + P_.tau_syn_exc) / (P_.tau_m * P_.tau_syn_exc)) / (P_.C_m * (P_.tau_m - P_.tau_syn_exc)); // as real
      

      V_.__P__V_m__I_kernel_inh__X__inh_spikes = 1.0 * P_.tau_m * P_.tau_syn_inh * (std::exp(V_.__h / P_.tau_m) - std::exp(V_.__h / P_.tau_syn_inh)) * std::exp((-V_.__h) * (P_.tau_m + P_.tau_syn_inh) / (P_.tau_m * P_.tau_syn_inh)) / (P_.C_m * (P_.tau_m - P_.tau_syn_inh)); // as real
      

      V_.__P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes = 1.0 * std::exp((-V_.__h) / P_.tau_syn_exc); // as real
      

      V_.__P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes = 1.0 * std::exp((-V_.__h) / P_.tau_syn_inh); // as real
  }
  else {    
      

      V_.RefractoryCounts = nest::Time(nest::Time::ms((double) (P_.t_ref))).get_steps(); // as integer
      

      V_.__h = __resolution; // as ms
      

      V_.__P__V_m__V_m = 1.0 * std::exp((-V_.__h) / P_.tau_m); // as real
      

      V_.__P__V_m__I_kernel_exc__X__exc_spikes = 1.0 * P_.tau_m * P_.tau_syn_exc * ((-std::exp(V_.__h / P_.tau_m)) + std::exp(V_.__h / P_.tau_syn_exc)) * std::exp((-V_.__h) * (P_.tau_m + P_.tau_syn_exc) / (P_.tau_m * P_.tau_syn_exc)) / (P_.C_m * (P_.tau_m - P_.tau_syn_exc)); // as real
      

      V_.__P__V_m__I_kernel_inh__X__inh_spikes = 1.0 * P_.tau_m * P_.tau_syn_inh * (std::exp(V_.__h / P_.tau_m) - std::exp(V_.__h / P_.tau_syn_inh)) * std::exp((-V_.__h) * (P_.tau_m + P_.tau_syn_inh) / (P_.tau_m * P_.tau_syn_inh)) / (P_.C_m * (P_.tau_m - P_.tau_syn_inh)); // as real
      

      V_.__P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes = 1.0 * std::exp((-V_.__h) / P_.tau_syn_exc); // as real
      

      V_.__P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes = 1.0 * std::exp((-V_.__h) / P_.tau_syn_inh); // as real
  }
}
void iaf_psc_exp_nestml::pre_run_hook() {
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


void iaf_psc_exp_nestml::update(nest::Time const & origin,const long from, const long to)
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
    double V_m__tmp = (-P_.E_L) * V_.__P__V_m__V_m + P_.E_L + S_.I_kernel_exc__X__exc_spikes * V_.__P__V_m__I_kernel_exc__X__exc_spikes + S_.I_kernel_inh__X__inh_spikes * V_.__P__V_m__I_kernel_inh__X__inh_spikes + S_.V_m * V_.__P__V_m__V_m - P_.I_e * V_.__P__V_m__V_m * P_.tau_m / P_.C_m + P_.I_e * P_.tau_m / P_.C_m - B_.I_stim_grid_sum_ * V_.__P__V_m__V_m * P_.tau_m / P_.C_m + B_.I_stim_grid_sum_ * P_.tau_m / P_.C_m;
    double I_kernel_exc__X__exc_spikes__tmp = S_.I_kernel_exc__X__exc_spikes * V_.__P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes;
    double I_kernel_inh__X__inh_spikes__tmp = S_.I_kernel_inh__X__inh_spikes * V_.__P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes;
    /* replace analytically solvable variables with precisely integrated values  */
    S_.V_m = V_m__tmp;
    S_.I_kernel_exc__X__exc_spikes = I_kernel_exc__X__exc_spikes__tmp;
    S_.I_kernel_inh__X__inh_spikes = I_kernel_inh__X__inh_spikes__tmp;
    S_.I_kernel_exc__X__exc_spikes += ((0.001 * B_.spike_inputs_grid_sum_[EXC_SPIKES - MIN_SPIKE_RECEPTOR])) / (1 / 1000.0);
    S_.I_kernel_inh__X__inh_spikes += ((0.001 * B_.spike_inputs_grid_sum_[INH_SPIKES - MIN_SPIKE_RECEPTOR])) / (1 / 1000.0);
  }
  else
  {  
    S_.r = S_.r - 1;
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
void iaf_psc_exp_nestml::handle(nest::DataLoggingRequest& e)
{
  B_.logger_.handle(e);
}


void iaf_psc_exp_nestml::handle(nest::SpikeEvent &e)
{
  assert(e.get_delay_steps() > 0);
  assert( e.get_rport() < B_.spike_inputs_.size() );

  double weight = e.get_weight();
  size_t nestml_buffer_idx = 0;
  if ( weight >= 0.0 )
  {
    nestml_buffer_idx = std::get<0>(rport_to_nestml_buffer_idx[e.get_rport()]);
  }
  else
  {
    nestml_buffer_idx = std::get<1>(rport_to_nestml_buffer_idx[e.get_rport()]);
    if ( nestml_buffer_idx == iaf_psc_exp_nestml::PORT_NOT_AVAILABLE )
    {
      nestml_buffer_idx = std::get<0>(rport_to_nestml_buffer_idx[e.get_rport()]);
    }
    weight = -weight;
  }
  B_.spike_inputs_[ nestml_buffer_idx - MIN_SPIKE_RECEPTOR ].add_value(
    e.get_rel_delivery_steps( nest::kernel().simulation_manager.get_slice_origin() ),
    weight * e.get_multiplicity() );
}

void iaf_psc_exp_nestml::handle(nest::CurrentEvent& e)
{
  assert(e.get_delay_steps() > 0);

  const double current = e.get_current();     // we assume that in NEST, this returns a current in pA
  const double weight = e.get_weight();
  get_I_stim().add_value(
               e.get_rel_delivery_steps( nest::kernel().simulation_manager.get_slice_origin()),
               weight * current );
}

