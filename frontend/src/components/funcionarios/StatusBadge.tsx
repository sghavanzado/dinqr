import React from 'react';
import { Chip } from '@mui/material';
import type { ChipProps } from '@mui/material';

export interface StatusBadgeProps extends Omit<ChipProps, 'color'> {
  status: string;
  type?: 'employee' | 'attendance' | 'leave' | 'evaluation' | 'payroll' | 'benefit';
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ 
  status, 
  type = 'employee', 
  ...props 
}) => {
  const getStatusConfig = (status: string, type: string) => {
    const configs: Record<string, Record<string, { color: ChipProps['color']; label?: string }>> = {
      employee: {
        'ATIVO': { color: 'success', label: 'Ativo' },
        'INATIVO': { color: 'error', label: 'Inativo' },
        'SUSPENSO': { color: 'warning', label: 'Suspenso' },
        'LICENCA': { color: 'info', label: 'Em Licença' },
        'FERIAS': { color: 'secondary', label: 'Em Férias' },
      },
      attendance: {
        'PRESENTE': { color: 'success', label: 'Presente' },
        'AUSENTE': { color: 'error', label: 'Ausente' },
        'ATRASO': { color: 'warning', label: 'Atraso' },
        'JUSTIFICADO': { color: 'info', label: 'Justificado' },
        'MEIO_PERIODO': { color: 'secondary', label: 'Meio Período' },
      },
      leave: {
        'PENDENTE': { color: 'warning', label: 'Pendente' },
        'APROVADO': { color: 'success', label: 'Aprovado' },
        'REJEITADO': { color: 'error', label: 'Rejeitado' },
        'EM_ANDAMENTO': { color: 'info', label: 'Em Andamento' },
        'CONCLUIDO': { color: 'success', label: 'Concluído' },
        'CANCELADO': { color: 'error', label: 'Cancelado' },
      },
      evaluation: {
        'NAO_INICIADO': { color: 'default', label: 'Não Iniciado' },
        'EM_ANDAMENTO': { color: 'info', label: 'Em Andamento' },
        'CONCLUIDO': { color: 'success', label: 'Concluído' },
        'ATRASADO': { color: 'error', label: 'Atrasado' },
        'REVISAO': { color: 'warning', label: 'Em Revisão' },
      },
      payroll: {
        'RASCUNHO': { color: 'default', label: 'Rascunho' },
        'PROCESSANDO': { color: 'info', label: 'Processando' },
        'PROCESSADO': { color: 'success', label: 'Processado' },
        'PAGO': { color: 'success', label: 'Pago' },
        'ERRO': { color: 'error', label: 'Erro' },
        'CANCELADO': { color: 'error', label: 'Cancelado' },
      },
      benefit: {
        'ATIVO': { color: 'success', label: 'Ativo' },
        'INATIVO': { color: 'error', label: 'Inativo' },
        'SUSPENSO': { color: 'warning', label: 'Suspenso' },
        'PENDENTE': { color: 'info', label: 'Pendente' },
        'EXPIRADO': { color: 'error', label: 'Expirado' },
      },
    };

    return configs[type]?.[status] || { color: 'default' as ChipProps['color'], label: status };
  };

  const config = getStatusConfig(status, type);

  return (
    <Chip
      label={config.label || status}
      color={config.color}
      size="small"
      variant="filled"
      {...props}
    />
  );
};

export default StatusBadge;
