import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import EventCard from './EventCard';

// Helper para envolver componentes con Router
const renderWithRouter = component => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('EventCard', () => {
  const mockEvent = {
    id: 1,
    name: 'Conferencia de Tecnología',
    description: 'Una conferencia sobre las últimas tendencias tecnológicas',
    location: 'Bogotá, Colombia',
    start_date: '2024-06-15T10:00:00',
    end_date: '2024-06-15T18:00:00',
    capacity: 100,
    available_capacity: 50,
    computed_status: 'scheduled',
    is_full: false,
  };

  it('renders event name', () => {
    renderWithRouter(<EventCard event={mockEvent} />);
    expect(screen.getByText('Conferencia de Tecnología')).toBeInTheDocument();
  });

  it('renders event description', () => {
    renderWithRouter(<EventCard event={mockEvent} />);
    expect(
      screen.getByText(/Una conferencia sobre las últimas tendencias tecnológicas/)
    ).toBeInTheDocument();
  });

  it('renders event location', () => {
    renderWithRouter(<EventCard event={mockEvent} />);
    expect(screen.getByText(/Bogotá, Colombia/)).toBeInTheDocument();
  });

  it('displays available capacity when not full', () => {
    renderWithRouter(<EventCard event={mockEvent} />);
    expect(screen.getByText(/50 de 100 disponibles/)).toBeInTheDocument();
  });

  it('displays full message when event is full', () => {
    const fullEvent = { ...mockEvent, is_full: true, available_capacity: 0 };
    renderWithRouter(<EventCard event={fullEvent} />);
    expect(screen.getByText('🔴 Lleno')).toBeInTheDocument();
  });

  it('renders status badge', () => {
    renderWithRouter(<EventCard event={mockEvent} />);
    expect(screen.getByText('Programado')).toBeInTheDocument();
  });

  it('has link to event detail', () => {
    renderWithRouter(<EventCard event={mockEvent} />);
    const links = screen.getAllByRole('link');
    expect(links.some(link => link.getAttribute('href') === '/events/1')).toBe(true);
  });
});
