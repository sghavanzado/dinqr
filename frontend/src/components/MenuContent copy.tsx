import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Stack from '@mui/material/Stack';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import AnalyticsRoundedIcon from '@mui/icons-material/AnalyticsRounded';
import PeopleRoundedIcon from '@mui/icons-material/PeopleRounded';
import AssignmentRoundedIcon from '@mui/icons-material/AssignmentRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import InfoRoundedIcon from '@mui/icons-material/InfoRounded';
import HelpRoundedIcon from '@mui/icons-material/HelpRounded';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import ImportContactsIcon from '@mui/icons-material/ImportContacts';
import RequestQuoteIcon from '@mui/icons-material/RequestQuote';
import ArticleIcon from '@mui/icons-material/Article';
import MiscellaneousServicesIcon from '@mui/icons-material/MiscellaneousServices';
import HomeRepairServiceIcon from '@mui/icons-material/HomeRepairService';

const mainListItems = [
  { text: 'Home', icon: <HomeRoundedIcon /> },
  { text: 'Analytics', icon: <AnalyticsRoundedIcon /> },
  { text: 'Clients', icon: <PeopleRoundedIcon /> },
  { text: 'Tasks', icon: <AssignmentRoundedIcon /> },
  { text: 'Notas', icon: <AssignmentRoundedIcon /> },
  { text: 'Lançamentos', icon: <AssignmentRoundedIcon /> },
  { text: 'Plano Contable', icon: <AssignmentRoundedIcon /> },
  { text: 'Tesouraria', icon: <AccountBalanceIcon  /> },
  { text: 'Livros e Contas Anuais', icon: <ImportContactsIcon /> },
  { text: 'Impostos', icon: <RequestQuoteIcon /> },
  { text: 'Exercícios', icon: <ArticleIcon /> },
  { text: 'Configuração', icon: <MiscellaneousServicesIcon /> },
  { text: 'Utilitários', icon: <HomeRepairServiceIcon /> },
];

const secondaryListItems = [
  { text: 'Settings', icon: <SettingsRoundedIcon /> },
  { text: 'About', icon: <InfoRoundedIcon /> },
  { text: 'Feedback', icon: <HelpRoundedIcon /> },
];

export default function MenuContent() {
  return (
    <Stack sx={{ flexGrow: 1, p: 1, justifyContent: 'space-between' }}>
      <List dense>
        {mainListItems.map((item, index) => (
          <ListItem key={index} disablePadding sx={{ display: 'block' }}>
            <ListItemButton selected={index === 0}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <List dense>
        {secondaryListItems.map((item, index) => (
          <ListItem key={index} disablePadding sx={{ display: 'block' }}>
            <ListItemButton>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Stack>
  );
}
