import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; 

import Eligibility from '../src/Eligibility'; 

vi.mock('../src/DataContext', () => ({
  useData: () => ({
    userData: {},
    result: {},
    setUserData: vi.fn(),
    setResult: vi.fn(),
  }),
}));

test('renders the form title and button correctly', () => {
  render(<Eligibility />);

  const title = screen.getByText(/Vérification d'Éligibilité/i);
  expect(title).toBeInTheDocument();

  const button = screen.getByRole('button', { name: /Lancer la prédiction IA/i });
  expect(button).toBeInTheDocument();
});